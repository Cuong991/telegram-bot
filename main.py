import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# --- Telegram Bot Token ---
TELEGRAM_TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

# --- Khởi tạo trình duyệt Chrome ---
def capture_fear_greed_index():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://coinmarketcap.com/vi/charts/fear-and-greed-index/")
        time.sleep(5)  # Chờ trang load hoàn toàn

        # Tìm phần tử chính chứa Chỉ số
        element = driver.find_element("xpath", '//div[contains(text(),"Chỉ số sợ hãi và tham lam của tiền điện tử CMC")]/ancestor::section')

        # Chụp toàn trang
        driver.save_screenshot("full_screenshot.png")

        # Lấy tọa độ
        location = element.location_once_scrolled_into_view
        size = element.size
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        # Crop
        image = Image.open("full_screenshot.png")
        cropped_image = image.crop((x, y, x + width, y + height))
        cropped_image.save("fear_greed_index.png")
        
        return "fear_greed_index.png"

    finally:
        driver.quit()

# --- Handler lệnh /start ---
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Xem chỉ số Sợ hãi & Tham lam", callback_data='fear_greed')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Chào bạn! Chọn chức năng bên dưới:', reply_markup=reply_markup)

# --- Handler khi bấm nút ---
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'fear_greed':
        query.edit_message_text(text="Đang lấy chỉ số, vui lòng chờ...")

        # Gọi hàm chụp ảnh
        img_path = capture_fear_greed_index()

        # Gửi ảnh
        context.bot.send_photo(chat_id=query.message.chat.id, photo=open(img_path, 'rb'))

        # Xóa file sau khi gửi
        os.remove(img_path)
        os.remove("full_screenshot.png")

# --- Main ---
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
        
