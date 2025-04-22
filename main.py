import os
import requests
import datetime
import pytz
import asyncio
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, JobQueue
)

# Token
TOKEN = "7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk"
# Chat ID nhận cảnh báo
YOUR_CHAT_ID = YOUR_CHAT_ID_HERE  # Điền vào đây

# API Fear & Greed
def get_fear_and_greed():
    try:
        url = "https://api.alternative.me/fng/"
        response = requests.get(url)
        data = response.json()
        value = int(data['data'][0]['value'])
        return value
    except Exception as e:
        print(f"Lỗi lấy Fear & Greed Index: {e}")
        return None

# API Dominance
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

# Lấy giờ VN
def get_vietnam_time():
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.datetime.now(vn_tz)
    month = now.month
    quarter = f"Quý {((month-1)//3)+1}"
    return now.strftime(f"%H:%M - %d/%m/%Y ({quarter})")

# Text trạng thái Fear Greed
def get_status_text(value):
    if value <= 24:
        return "Sợ hãi tột độ🔴"
    elif 25 <= value <= 49:
        return "Sợ hãi🟠"
    elif 50 <= value <= 54:
        return "Trung lập🔵"
    elif 55 <= value <= 74:
        return "Tham lam🟢"
    else:
        return "Tham lam tột độ🟢⚡"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Chỉ số Tham lam & Sợ hãi Crypto", callback_data="check_fear_greed")],
        [InlineKeyboardButton("Chỉ số Bitcoin Dominance & Altcoin", callback_data="check_dominance")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⭐Chọn chức năng thực hiện⭐: More to come soon!", reply_markup=reply_markup)

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Các lệnh hỗ trợ:\n\n"
        "/start - Bắt đầu sử dụng bot\n"
        "/help - Xem hướng dẫn các lệnh\n\n"
        "👉 Admin hỗ trợ: @cuong49"
    )
    await update.message.reply_text(help_text)

# Xử lý bấm nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data == "check_fear_greed":
        value = get_fear_and_greed()
        if value is not None:
            status_text = get_status_text(value)
            vietnam_time = get_vietnam_time()
            message = (
                f">>Chỉ số Tham lam & Sợ hãi hiện tại: 👉 <b>{value}</b>\n\n"
                f"Thời gian: {vietnam_time}\n\n"
                f"- <b>Trạng thái:</b> {status_text}\n\n"
                f"🔴 = sợ hãi tột độ\n"
                f"🟠 = sợ hãi\n"
                f"🔵 = trung lập\n"
                f"🟢 = tham lam\n"
                f"🟢⚡ = tham lam tột độ\n\n"
                f"<b>Admin</b>: @cuong49"
            )
        else:
            message = "Không thể lấy dữ liệu chỉ số. Vui lòng thử lại sau."
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")

    elif query.data == "check_dominance":
        btc_dominance, altcoin_dominance = get_dominance_data()
        if btc_dominance is not None:
            vietnam_time = get_vietnam_time()
            if altcoin_dominance < 45:
                season_chance = "Thấp 🔻"
            elif 45 <= altcoin_dominance < 55:
                season_chance = "Trung bình ⚖️"
            elif 55 <= altcoin_dominance < 65:
                season_chance = "Khả năng sắp diễn ra cao 🚀"
            else:
                season_chance = "Altcoin season đang diễn ra 🌟"

            message = (
                f">>Chỉ số Bitcoin Dominance hiện tại: 👉 <b>{btc_dominance}%</b>\n\n"
                f"Chỉ số Altcoin Dominance hiện tại: 👉 <b>{altcoin_dominance}%</b>\n\n"
                f"Thời gian: {vietnam_time}\n\n"
                f"Khả năng altcoin season diễn ra: <b>{season_chance}</b>\n\n"
                f"- <b>Ghi chú:</b> Chỉ số Altcoin Dominance càng cao thì khả năng Altcoin Season càng mạnh.\n\n"
                f"<b>Admin</b>: @cuong49"
            )
        else:
            message = "Không thể lấy dữ liệu Dominance. Vui lòng thử lại sau."
        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")

# Cảnh báo tự động
async def send_warning_alert(context: ContextTypes.DEFAULT_TYPE):
    value = get_fear_and_greed()
    if value is not None:
        message = None
        if value >= 75:
            message = (
                f"⚡⚡⚡ CẢNH BÁO: Tham lam cực đại!\nChỉ số: {value}\n<b>Admin</b>: @cuong49"
            )
        elif value <= 20:
            message = (
                f"⚠️⚠️⚠️ CẢNH BÁO: Sợ hãi tột độ!\nChỉ số: {value}\n<b>Admin</b>: @cuong49"
            )

        if message:
            await context.bot.send_message(chat_id=YOUR_CHAT_ID, text=message, parse_mode="HTML")

# Hàm main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button))

    app.job_queue.run_repeating(send_warning_alert, interval=3600, first=10)

    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
            
