import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TELEGRAM_TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

def capture_fear_greed_index():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Headless mới
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Opening the web page...")
        driver.get("https://coinmarketcap.com/vi/charts/fear-and-greed-index/")
        time.sleep(5)  # Chờ trang load hoàn toàn

        # Full screenshot
        driver.save_screenshot('full_screenshot.png')
        print("Full screenshot taken.")

        # Tìm đúng phần tử cần crop
        element = driver.find_element("xpath", '//div[contains(@class, "iULUNk")]')  # Cập nhật lại xpath nếu cần
        location = element.location
        size = element.size

        print(f"Element found at {location} with size {size}")

        # Chuyển tọa độ và kích thước ra hình ảnh
        x = int(location['x'])
        y = int(location['y'])
        width = int(size['width'])
        height = int(size['height'])

        # Crop ảnh
        im = Image.open('full_screenshot.png')
        im_cropped = im.crop((x, y, x + width, y + height))
        im_cropped.save('fear_greed_index.png')

        print("Image cropped and saved as 'fear_greed_index.png'")

        return 'fear_greed_index.png'

    except Exception as e:
        print(f"Error during screenshot or crop: {e}")
        return None

    finally:
        driver.quit()

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

    # Gọi hàm chụp ảnh
    img_path = capture_fear_greed_index()

    if img_path and os.path.exists(img_path):
        print(f"File {img_path} exists, sending photo.")
        with open(img_path, 'rb') as photo:
            await query.message.reply_photo(photo, caption="Chỉ số Sợ hãi & Tham lam hiện tại:")

        # Xóa file sau khi gửi
        os.remove(img_path)
        os.remove('full_screenshot.png')
    else:
        print("Error: File not found or capture failed.")
        await query.message.reply_text('Có lỗi khi lấy ảnh. Vui lòng thử lại sau!')

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == '__main__':
    main()
    
