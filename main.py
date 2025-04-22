from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from io import BytesIO
from PIL import Image

# === Config ===
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'  # Thay bằng token bot của bạn
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
            chrome_options.add_argument('--headless')  # Chạy không hiển thị giao diện
            driver = webdriver.Chrome(options=chrome_options)
            
            # Mở trang web
            driver.get(TARGET_URL)
            
            # Tìm phần tử chứa chỉ số
            element = driver.find_element_by_css_selector('.fear-greed-index')  # Thay bằng CSS selector thực tế
            
            # Chụp ảnh phần tử
            location = element.location
            size = element.size
            screenshot = driver.get_screenshot_as_png()
            
            # Cắt ảnh
            image = Image.open(BytesIO(screenshot))
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']
            cropped_image = image.crop((left, top, right, bottom))
            
            # Lưu ảnh vào bộ nhớ
            img_byte_arr = BytesIO()
            cropped_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Gửi ảnh
            await query.message.reply_photo(
                photo=img_byte_arr,
                caption="Chỉ số tham lam và sợ hãi hiện tại!"
            )
            
            driver.quit()
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
