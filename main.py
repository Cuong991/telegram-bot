import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time

TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'

# Hàm lấy dữ liệu thanh lý từ Binance
def get_binance_liquidation_data():
    url = 'https://fapi.binance.com/fapi/v1/allForceOrders'
    end_time = int(time.time() * 1000)
    start_time = end_time - (24 * 60 * 60 * 1000)

    params = {
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data:
        total_liquidations = len(data)
        total_value = sum([float(order['price']) * float(order['origQty']) for order in data])
        max_liquidation = max(data, key=lambda x: float(x['price']) * float(x['origQty']))
        max_value = float(max_liquidation['price']) * float(max_liquidation['origQty'])

        return f"Trong vòng 24 giờ qua, đã có {total_liquidations} nhà giao dịch bị thanh lý, tổng giá trị thanh lý là ${total_value/1e6:.2f} million.\n" \
               f"Lệnh thanh lý lớn nhất xảy ra trên {max_liquidation['symbol']} - {max_liquidation['symbol']} giá trị là ${max_value/1e6:.2f}M."
    else:
        return "Không tìm thấy dữ liệu thanh lý."

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Chào bạn! Tôi sẽ lấy dữ liệu thanh lý từ Binance. Đợi một chút...")

# Hàm xử lý lệnh lấy dữ liệu thanh lý
async def get_liquidation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = get_binance_liquidation_data()
    await update.message.reply_text(data)

# Khởi tạo bot
def main():
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("get_liquidation", get_liquidation))

    # Chạy bot với chế độ polling (không cần asyncio.run())
    application.run_polling()

# Chạy bot
if __name__ == "__main__":
    main()
        
