import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes# === Config ===
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'  # <-- thay bằng token bot của bạn
SCREENSHOT_API = 'https://image.thum.io/get/fullpage/https://coinmarketcap.com/vi/charts/fear-and-greed-index/'# === Setup logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)# === Start command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Xem chỉ số tham lam & sợ hãi", callback_data='fear_greed')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chào bạn! Chọn chức năng bên dưới:', reply_markup=reply_markup)# === Handle button press ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
if query.data == 'fear_greed':
    # Tải ảnh chụp web
    image_url = SCREENSHOT_API
    response = requests.get(image_url)

    if response.status_code == 200:
        await query.message.reply_photo(
            photo=response.content,
            caption="Chỉ số tham lam và sợ hãi hiện tại, xem chi tiết trong ảnh nhé!"
        )
    else:
        await query.message.reply_text('Không lấy được ảnh. Thử lại sau!')
# === Main ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()if __name__ == '__main__':
    main() 



