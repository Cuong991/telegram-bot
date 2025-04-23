import logging
import aiohttp
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'  # <-- Thay token của bạn vào

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Lấy dữ liệu thanh lý mới nhất", callback_data='get_liquidation')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chào bạn! Bấm nút bên dưới để lấy dữ liệu:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'get_liquidation':
        await query.edit_message_text(text="Đang lấy dữ liệu mới nhất, vui lòng chờ...")

        data = await get_liquidation_data()

        await query.edit_message_text(text=data)

async def get_liquidation_data():
    url = "https://fapi.binance.com/fapi/v1/allForceOrders"

    now = datetime.datetime.utcnow()
    past = now - datetime.timedelta(hours=24)

    params = {
        "startTime": int(past.timestamp() * 1000),
        "endTime": int(now.timestamp() * 1000),
        "limit": 1000  # Binance tối đa 1000 lệnh mỗi lần
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        total_traders = 0
        total_value = 0
        largest_liquidation = 0
        largest_symbol = ""
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()

                if isinstance(data, list):
                    for order in data:
                        total_traders += 1
                        value = float(order['price']) * float(order['origQty'])
                        total_value += value

                        if value > largest_liquidation:
                            largest_liquidation = value
                            largest_symbol = order['symbol']

                    if total_traders == 0:
                        return "Không có lệnh thanh lý nào trong 24 giờ qua."

                    text = (
                        f"Trong vòng 24 giờ qua, đã có {total_traders:,} lệnh thanh lý, "
                        f"tổng giá trị thanh lý là ${total_value/1_000_000:.2f}M.\n"
                        f"Lệnh thanh lý lớn nhất: {largest_symbol} trị giá ${largest_liquidation/1_000_000:.2f}M."
                    )
                    return text
                else:
                    return "Không thể lấy dữ liệu từ Binance."
    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
    
