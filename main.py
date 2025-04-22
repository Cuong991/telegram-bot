import time
import os
from selenium import webdriver
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from PIL import Image
from io import BytesIO

# API token của bạn
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

# Hàm chụp ảnh màn hình trang web
def screenshot_feargreed():
    try:
        # Khởi tạo Selenium với Chrome WebDriver
        options = webdriver.ChromeOptions()
        options.headless = True  # Chạy ẩn không mở cửa sổ trình duyệt
        driver = webdriver.Chrome(options=options)

        # Truy cập trang web Fear & Greed Index
        driver.get("https://www.coinglass.com/vi/pro/i/FearGreedIndex")
        time.sleep(3)  # Đợi trang web tải xong

        # Lưu ảnh chụp màn hình
        screenshot_path = "/tmp/fear_greed_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()

        # Kiểm tra nếu ảnh đã được lưu
        if not os.path.exists(screenshot_path):
            raise Exception("Không thể lưu ảnh chụp màn hình.")

        # Mở ảnh đã chụp để xử lý
        img = Image.open(screenshot_path)
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
    
