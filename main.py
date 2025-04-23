import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import time

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

# Dùng Selenium để lấy dữ liệu thanh lý từ trang web
def get_liquidation_data():
    url = "https://www.coinglass.com/vi/LiquidationData"

    try:
        # Cấu hình và khởi tạo WebDriver (Chrome)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Chạy Chrome ở chế độ không hiển thị giao diện (headless)
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Tạo WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Mở trang web
        driver.get(url)

        # Chờ trang web tải xong
        time.sleep(5)  # Chờ 5 giây để dữ liệu tải đầy đủ

        # Tìm và lấy nội dung thanh lý
        try:
            # Lấy phần chứa thông tin thanh lý
            liquidation_section = driver.find_element(By.CSS_SELECTOR, 'div.index_title__x6mnK')
            liquidation_text = liquidation_section.text
        except Exception as e:
            liquidation_text = f"Không thể lấy dữ liệu thanh lý: {e}"

        driver.quit()
        return liquidation_text

    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
        
