import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram.ext import ContextTypes

# Thay đổi token của bạn tại đây
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

# Hàm lấy dữ liệu Crypto Cap của TOTAL2 từ TradingView
def get_crypto_cap():
    # Cấu hình Selenium để chạy trình duyệt không giao diện
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Không mở cửa sổ trình duyệt
    chrome_driver_path = "/path/to/chromedriver"  # Đảm bảo đường dẫn đúng đến chromedriver

    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    driver.get("https://vn.tradingview.com/chart/?symbol=CRYPTOCAP%3ATOTAL2")

    # Đợi trang web tải xong
    time.sleep(10)

    try:
        # Tìm chỉ số Crypto Cap của TOTAL2
        price_element = driver.find_element(By.XPATH, '//*[@id="tv-widget-market-summary"]/div[1]/div[1]/span[1]')
        price = price_element.text

        # Đóng trình duyệt sau khi lấy dữ liệu
        driver.quit()

        return price
    except Exception as e:
        driver.quit()
        return f"Đã xảy ra lỗi khi lấy dữ liệu: {e}"

# Hàm xử lý lệnh /start và tạo nút
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Gửi nút chức năng cho người dùng
    keyboard = [
        [InlineKeyboardButton("Lấy dữ liệu Crypto Cap", callback_data='get_cap')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Chào bạn! Nhấn nút dưới đây để lấy dữ liệu Crypto Cap (TOTAL2) hiện tại:", reply_markup=reply_markup)

# Hàm xử lý khi người dùng nhấn nút
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'get_cap':
        # Lấy dữ liệu Crypto Cap
        price = get_crypto_cap()

        # Gửi kết quả về người dùng với icon và văn bản trang trí
        if "lỗi" in price:
            await query.edit_message_text(f"❌ Đã xảy ra lỗi khi lấy dữ liệu: {price}")
        else:
            await query.edit_message_text(f"📊 **Dữ liệu Crypto Cap hiện tại:**\n\n💰 **TOTAL2**: {price} USD\n\n🕒 Cập nhật theo thời gian thực.")

# Hàm chính để chạy bot
def main() -> None:
    # Khởi tạo Application với token của bạn
    application = Application.builder().token(TOKEN).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Bắt đầu bot
    application.run_polling()

if __name__ == "__main__":
    main()
    
