import time
from selenium import webdriver
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
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
        img_byte_arr = screenshot_feargreed()

        # Gửi ảnh cho người dùng
        await query.message.reply_text("Đây là Chỉ số Sợ hãi và Tham lam hiện tại:")
        await query.message.reply_photo(photo=img_byte_arr)

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
    
