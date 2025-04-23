import logging
import httpx
from selectolax.parser import HTMLParser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'  # <-- Thay token vào

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
    url = "https://www.coinglass.com/vi/LiquidationData"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "vi-VN,vi;q=0.9",
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            html = HTMLParser(response.text)

            # Tìm tất cả text trong trang
            all_text_nodes = html.css('body *')

            for node in all_text_nodes:
                text = node.text(strip=True)
                if text and "trong vòng 24 giờ qua" in text.lower():
                    return text

            return "Không tìm thấy dữ liệu thanh lý."

    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
        
