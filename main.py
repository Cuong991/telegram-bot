import logging
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'  # <-- Thay token của bạn vào đây

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Lấy dữ liệu thanh lý mới nhất", callback_data='get_liquidation')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chào bạn! Bấm nút bên dưới để lấy dữ liệu:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'get_liquidation':
        # Thông báo chờ
        await query.edit_message_text(text="Đang lấy dữ liệu mới nhất, vui lòng chờ...")

        # Lấy dữ liệu từ website
        data = await asyncio.to_thread(scrape_liquidation_data)

        # Gửi dữ liệu lấy được
        await query.edit_message_text(text=data)

def scrape_liquidation_data():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        driver.get('https://www.coinglass.com/vi/LiquidationData')

        # Đợi tối đa 15 giây cho đến khi phần tử có nội dung xuất hiện
        wait = WebDriverWait(driver, 15)
        container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'index_lqData__il52W')))

        data_text = container.text

        # Chỉ lấy đoạn văn bản chính cần thiết
        if data_text:
            return f"Dữ liệu thanh lý mới nhất:\n\n{data_text}"
        else:
            return "Không tìm thấy dữ liệu thanh lý. Có thể website thay đổi giao diện?"

    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"
    finally:
        driver.quit()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
            
