import logging
import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'  # <-- Thay token Telegram bot bạn vào đây

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
    url = "https://fapi.coinglass.com/api/futures/liquidation_chart?timeType=24h"

    headers = {
        "origin": "https://www.coinglass.com",
        "referer": "https://www.coinglass.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                result = await response.json()

                if result.get("success"):
                    total_liquidation = result["data"]["totalVolUsd"]
                    total_traders = result["data"]["totalLiquidated"]
                    largest_liq = result["data"]["maxSingleLiquidation"]
                    largest_exchange = result["data"]["maxSingleLiquidationExchange"]
                    largest_symbol = result["data"]["maxSingleLiquidationSymbol"]

                    text = (
                        f"Trong vòng 24 giờ qua, đã có {total_traders:,} nhà giao dịch bị thanh lý, "
                        f"tổng giá trị thanh lý là ${total_liquidation/1_000_000:.2f}M.\n"
                        f"Lệnh thanh lý lớn nhất xảy ra trên {largest_exchange} - {largest_symbol} "
                        f"giá trị là ${largest_liq/1_000_000:.2f}M."
                    )
                    return text
                else:
                    return "Không thể lấy dữ liệu từ Coinglass. Có thể API thay đổi?"
    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
    
