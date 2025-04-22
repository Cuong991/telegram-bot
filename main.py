import logging
import time
import os
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# === Config ===
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'  # <-- thay bằng token bot của bạn
SCREENSHOT_API = 'https://www.coinglass.com/vi/pro/i/FearGreedIndex'

# === Setup logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === Chụp ảnh màn hình trang web Fear & Greed Index ===
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
        img_byte_arr.seek(0)

        return img_byte_arr
    except Exception as e:
        print(f"Error in screenshot_feargreed: {e}")
        raise e

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
        # Chụp ảnh màn hình trang web
        try:
            img_byte_arr = screenshot_feargreed()
            await query.message.reply_photo(
                photo=img_byte_arr,
                caption="Đây là Chỉ số Tham Lam và Sợ Hãi hiện tại. Hãy xem chi tiết trong ảnh!"
            )
        except Exception as e:
            print(f"Error: {e}")
            await query.message.reply_text('Không thể lấy ảnh, vui lòng thử lại sau.')

# === Main function ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Thêm các handler cho các lệnh và nút bấm
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    # Bắt đầu bot và lắng nghe sự kiện
    app.run_polling()

if __name__ == '__main__':
    main()
    
