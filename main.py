import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def capture_fear_greed_index():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Headless mới
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://coinmarketcap.com/vi/charts/fear-and-greed-index/"
    driver.get(url)
    time.sleep(5)

    # Full screenshot
    driver.save_screenshot('full_screenshot.png')

    # Tìm đúng phần tử cần crop
    element = driver.find_element("xpath", '//div[contains(@class, "iULUNk")]')  # Update xpath nếu cần

    location = element.location
    size = element.size
    driver.quit()

    x = int(location['x'])
    y = int(location['y'])
    width = int(size['width'])
    height = int(size['height'])

    im = Image.open('full_screenshot.png')
    im_cropped = im.crop((x, y, x + width, y + height))
    im_cropped.save('fear_greed_index.png')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Xem chỉ số Sợ hãi & Tham lam", callback_data='fear_greed')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chọn chức năng:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Đang lấy chỉ số, vui lòng chờ...")

    capture_fear_greed_index()

    with open('fear_greed_index.png', 'rb') as photo:
        await query.message.reply_photo(photo, caption="Chỉ số Sợ hãi & Tham lam hiện tại:")

    os.remove('full_screenshot.png')
    os.remove('fear_greed_index.png')

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == '__main__':
    main()
    
