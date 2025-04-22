import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import nest_asyncio
import asyncio
import datetime
import pytz

# Token Telegram Bot
TOKEN = "YOUR_TOKEN_HERE"

# Hàm lấy chỉ số Fear & Greed
def get_fear_and_greed():
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url)
        data = response.json()
        return int(data['data'][0]['value'])
    except Exception as e:
        print(f"Lỗi lấy Fear & Greed Index: {e}")
        return None

# Hàm lấy Bitcoin Dominance
def get_dominance_data():
    try:
        url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(url)
        data = response.json()
        btc_dominance = data['data']['market_cap_percentage']['btc']
        altcoin_dominance = 100 - btc_dominance
        return round(btc_dominance, 2), round(altcoin_dominance, 2)
    except Exception as e:
        print(f"Lỗi lấy Dominance: {e}")
        return None, None

# Hàm lấy giờ Việt Nam
def get_vietnam_time():
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.datetime.now(vn_tz)
    month = now.month
    quarter = f"Quý {(month-1)//3 +1}"
    return now.strftime(f"%H:%M - %d/%m/%Y ({quarter})")

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Chỉ số Fear & Greed", callback_data="fear_greed")],
        [InlineKeyboardButton("Dominance BTC/Altcoin", callback_data="dominance")],
        [InlineKeyboardButton("Thông tin thêm", callback_data="extra_info")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⭐ Chọn chức năng:", reply_markup=reply_markup)

# Lệnh /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Các lệnh hỗ trợ:\n/start - Bắt đầu\n/help - Hướng dẫn\n\nAdmin hỗ trợ: @youradmin"
    )

# Xử lý khi bấm nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "fear_greed":
        value = get_fear_and_greed()
        if value is not None:
            message = f"Chỉ số Fear & Greed hiện tại: {value}\n\nThời gian: {get_vietnam_time()}"
        else:
            message = "Không lấy được dữ liệu chỉ số."
        await query.message.reply_text(message)

    elif query.data == "dominance":
        btc, alt = get_dominance_data()
        if btc is not None:
            message = f"Bitcoin Dominance: {btc}%\nAltcoin Dominance: {alt}%\n\nThời gian: {get_vietnam_time()}"
        else:
            message = "Không lấy được dữ liệu dominance."
        await query.message.reply_text(message)

    elif query.data == "extra_info":
        await query.message.reply_text("Đây là thông tin thêm bạn yêu cầu!")

# Hàm main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
    
