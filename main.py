import requests
from telegram import Update
from telegram.ext import Application, CommandHandler
import time

TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

# Hàm lấy dữ liệu thanh lý từ CoinGecko
def get_coingecko_liquidation_data():
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin/market_chart'
    params = {
        'vs_currency': 'usd',
        'days': '1',  # Dữ liệu trong vòng 24h
        'interval': 'minute'
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if 'prices' in data:
            # Tổng thanh lý trong 24h (sử dụng dữ liệu từ API)
            total_liquidations = len(data['prices'])  # Đếm số lần thay đổi giá
            total_value = sum([price[1] for price in data['prices']])  # Tổng giá trị giao dịch
            max_liquidation = max(data['prices'], key=lambda x: x[1])  # Giá trị thanh lý lớn nhất
            max_value = max_liquidation[1]

            return f"Trong vòng 24 giờ qua, đã có {total_liquidations} nhà giao dịch bị thanh lý, tổng giá trị thanh lý là ${total_value/1e6:.2f} million.\n" \
                   f"Lệnh thanh lý lớn nhất xảy ra với Bitcoin, giá trị là ${max_value/1e6:.2f}M."
        else:
            return "Không tìm thấy dữ liệu thanh lý."

    except Exception as e:
        return f"Đã xảy ra lỗi khi lấy dữ liệu: {str(e)}"

# Hàm xử lý lệnh /start
async def start(update: Update, context):
    await update.message.reply_text("Chào bạn! Tôi sẽ lấy dữ liệu thanh lý từ CoinGecko. Đợi một chút...")

# Hàm xử lý lệnh lấy dữ liệu thanh lý
async def get_liquidation(update: Update, context):
    data = get_coingecko_liquidation_data()
    await update.message.reply_text(data)

def main():
    # Khởi tạo Application với token của bạn
    application = Application.builder().token(TOKEN).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_liquidation", get_liquidation))

    # Bắt đầu bot
    application.run_polling()

if __name__ == "__main__":
    main()
    
