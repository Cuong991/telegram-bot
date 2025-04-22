import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import nest_asyncio
import asyncio
import datetime
import pytz

# Token của bạn
TOKEN = "YOUR_TOKEN_HERE"

# Hàm lấy Fear & Greed Index
def get_fear_and_greed():
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url)
        data = response.json()
        return int(data['data'][0]['value'])
    except Exception as e:
        print(f"Lỗi lấy Fear & Greed Index: {e}")
        return None

# Hàm lấy thời gian Việt Nam
def get_vietnam_time():
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.datetime.now(vn_tz)
    month = now.month
    quarter = f"Quý {(month-1)//3 +1}"
    return now.strftime(f"%H:%M - %d/%m/%Y ({quarter})")

# Hàm lấy Dominance
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

# Hàm khi gõ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Chỉ số Fear & Greed", callback_data="check_fear_greed")],
        [InlineKeyboardButton("Dominance BTC/Altcoin", callback_data="check_dominance")],
        [InlineKeyboardButton("TÊN NÚT MỚI", callback_data="new_button")]  # <<< THÊM NÚT MỚI Ở ĐÂY
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⭐Chọn chức năng:", reply_markup=reply_markup)

# Hàm khi gõ /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Bắt đầu\n/help - Hướng dẫn")

# Hàm xử lý khi bấm nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "check_fear_greed":
        value = get_fear_and_greed()
        if value is not None:
            message = f"Chỉ số hiện tại: {value}\nThời gian: {get_vietnam_time()}"
        else:
            message = "Không lấy được dữ liệu."
        await query.message.reply_text(message)

    elif query.data == "check_dominance":
        btc, alt = get_dominance_data()
        if btc is not None:
            message = f"Dominance BTC: {btc}%\nDominance Altcoin: {alt}%\nThời gian: {get_vietnam_time()}"
        else:
            message = "Không lấy được dữ liệu."
        await query.message.reply_text(message)

    elif query.data == "new_button":
        await query.message.reply_text("Bạn vừa bấm nút mới!")  # <<< XỬ LÝ NÚT MỚI Ở ĐÂY

# Hàm chính
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
