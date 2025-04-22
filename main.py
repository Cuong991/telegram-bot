from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === Config ===
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'
TARGET_URL = 'https://coinmarketcap.com/vi/charts/fear-and-greed-index/'

# === Setup logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === Start command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Xem chỉ số tham lam và sợ hãi", callback_data='fear_greed')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chào bạn! Chọn chức năng bên dưới:', reply_markup=reply_markup)

# === Handle button press ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'fear_greed':
        try:
            # Cấu hình Selenium
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(TARGET_URL)
            driver.implicitly_wait(5)  # Chờ 5 giây để trang tải

            # Chụp màn hình
            screenshot = driver.get_screenshot_as_png()
            driver.quit()

            await query.message.reply_photo(
                photo=screenshot,
                caption="Chỉ số tham lam và sợ hãi hiện tại!"
            )
        except Exception as e:
            logging.error(f"Error capturing screenshot: {e}")
            await query.message.reply_text('Không lấy được ảnh. Thử lại sau!')

# === Main ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == '__main__':
    main()
