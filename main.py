import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image
import io
import time

TOKEN = "7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk"

# Hàm chụp màn hình 1 khu vực
async def capture_chart():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://coinmarketcap.com/vi/charts/fear-and-greed-index/")
    time.sleep(5)  # Đợi web load

    # Tìm đúng khu vực chỉ số
    element = driver.find_element(By.XPATH, "//div[contains(@class,'sc-54d73334-0')]")
    location = element.location
    size = element.size

    # Chụp full màn hình
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    image = Image.open(io.BytesIO(screenshot))

    # Cắt đúng khu vực chỉ số
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    cropped_image = image.crop((left, top, right, bottom))

    # Lưu vào bộ nhớ
    output = io.BytesIO()
    cropped_image.save(output, format='PNG')
    output.seek(0)
    return output

# Hàm gửi ảnh và text
async def send_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    photo = await capture_chart()
    await context.bot.send_photo(chat_id=chat_id, photo=photo, caption="Chỉ số tham lam và sợ hãi hiện tại:")

# Hàm /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Xem chỉ số tham lam và sợ hãi", callback_data='fear_greed')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chọn một chức năng:', reply_markup=reply_markup)

# Xử lý khi bấm nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'fear_greed':
        await send_chart(update, context)

# Main
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
    
