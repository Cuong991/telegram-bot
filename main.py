import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from io import BytesIO
from PIL import Image

# API token của bạn
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

# Hàm chụp ảnh màn hình trang web
def screenshot_feargreed():
    try:
        # Khởi tạo Selenium với Chrome WebDriver
        options = Options()
        options.add_argument("--headless")  # Chạy không giao diện
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = '/usr/bin/chromium'  # Dùng Chrome được cài trong Docker

        driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", options=options)

        # Truy cập trang web Fear & Greed Index
        driver.get("https://www.coinglass.com/vi/pro/i/FearGreedIndex")
        time.sleep(3)  # Đợi trang web tải xong

        # Lưu ảnh chụp màn hình
        screenshot = driver.get_screenshot_as_png()
        driver.quit()

        # Mở ảnh đã chụp
        img_byte_arr = BytesIO(screenshot)
        img = Image.open(img_byte_arr)
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        return img_byte_arr
    except Exception as e:
        print(f"Error in screenshot_feargreed: {e}")
        raise e

# Hàm xử lý lệnh /start và nút chọn chức năng
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Xem Chỉ số Sợ hãi và Tham lam", callback_data='feargreed')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chọn một chức năng:', reply_markup=reply_markup)

# Hàm xử lý nút "Xem Chỉ số Sợ hãi và Tham lam"
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'feargreed':
        # Chụp ảnh màn hình trang web
        try:
            img_byte_arr = screenshot_feargreed()
            await query.message.reply_text("Đây là Chỉ số Sợ hãi và Tham lam hiện tại:")
            await query.message.reply_photo(photo=img_byte_arr)
        except Exception as e:
            print(f"Error: {e}")
            await query.message.reply_text("Có lỗi xảy ra khi chụp ảnh màn hình.")

# Hàm main để khởi chạy bot
def main() -> None:
    # Khởi tạo ứng dụng và thêm handler
    application = Application.builder().token(TOKEN).build()

    # Thêm handler cho lệnh /start
    application.add_handler(CommandHandler("start", start))

    # Thêm handler cho các nút bấm
    application.add_handler(CallbackQueryHandler(button))

    # Bắt đầu bot
    application.run_polling()

if __name__ == '__main__':
    main()
    
