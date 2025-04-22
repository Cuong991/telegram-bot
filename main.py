import time
from selenium import webdriver
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext, Update
from PIL import Image
from io import BytesIO

# API token của bạn
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

# Hàm chụp ảnh màn hình trang web
def screenshot_feargreed():
    # Khởi tạo Selenium với Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.headless = True  # Chạy ẩn không mở cửa sổ trình duyệt
    driver = webdriver.Chrome(options=options)

    # Truy cập trang web Fear & Greed Index
    driver.get("https://www.coinglass.com/vi/pro/i/FearGreedIndex")
    time.sleep(3)  # Đợi trang web tải xong

    # Chụp ảnh màn hình
    screenshot_path = "/tmp/fear_greed_screenshot.png"
    driver.save_screenshot(screenshot_path)
    driver.quit()

    # Mở ảnh đã chụp để xử lý thêm nếu cần (ví dụ: cắt ảnh, thêm thông tin)
    img = Image.open(screenshot_path)
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return img_byte_arr

# Hàm xử lý lệnh /start và nút chọn chức năng
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Xem Chỉ số Sợ hãi và Tham lam", callback_data='feargreed')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Chọn một chức năng:', reply_markup=reply_markup)

# Hàm xử lý nút "Xem Chỉ số Sợ hãi và Tham lam"
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'feargreed':
        # Chụp ảnh màn hình trang web
        img_byte_arr = screenshot_feargreed()

        # Gửi ảnh cho người dùng
        query.message.reply_text("Đây là Chỉ số Sợ hãi và Tham lam hiện tại:")
        query.message.reply_photo(photo=img_byte_arr)

# Hàm main để khởi chạy bot
def main() -> None:
    updater = Updater(TOKEN)

    # Lấy dispatcher để thêm handler
    dispatcher = updater.dispatcher

    # Thêm handler cho lệnh /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Thêm handler cho các nút bấm
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Bắt đầu bot
    updater.start_polling()

    # Chạy bot cho đến khi bị dừng
    updater.idle()

if __name__ == '__main__':
    main()
    
