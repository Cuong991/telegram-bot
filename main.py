import logging
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Lấy dữ liệu thanh lý", callback_data='get_liquidation')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chào bạn! Bấm nút bên dưới để lấy dữ liệu:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'get_liquidation':
        # Gửi thông báo chờ
        await query.edit_message_text(text="Đang lấy dữ liệu, vui lòng đợi...")

        # Lấy dữ liệu từ web
        data = scrape_liquidation_data()

        # Gửi dữ liệu
        await query.message.reply_text(data)

def scrape_liquidation_data():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get('https://www.coinglass.com/vi/LiquidationData')
        # Đợi trang load (tuỳ chỉnh thời gian nếu mạng chậm)
        driver.implicitly_wait(10)

        # Tìm phần chứa thông tin
        element = driver.find_element(By.CLASS_NAME, 'index_lqData__il52W')
        data_text = element.text

        return f"Dữ liệu thanh lý:\n{data_text}"
    except Exception as e:
        return f"Đã xảy ra lỗi: {e}"
    finally:
        driver.quit()

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
        
