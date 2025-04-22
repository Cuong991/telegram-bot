import os
import requests
from io import BytesIO
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import nest_asyncio
import asyncio

# Token của bạn
TOKEN = "YOUR_BOT_TOKEN"

# Hàm xử lý khi bấm nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data == "check_fear_greed":
        target_url = "https://coinmarketcap.com/vi/"  # URL bạn muốn chụp
        screenshot_url = f"https://image.thum.io/get/fullpage/{target_url}?wait=5"

        try:
            response = requests.get(screenshot_url)
            if response.status_code == 200:
                image = BytesIO(response.content)
                image.seek(0)

                text_message = "Chỉ số Tham lam & Sợ hãi hiện tại như hình dưới nhé:"
                await context.bot.send_photo(chat_id=chat_id, photo=image, caption=text_message)
            else:
                await context.bot.send_message(chat_id=chat_id, text="Không thể lấy ảnh từ website.")
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"Lỗi: {e}")

# Hàm xử lý khi gõ /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Xem Chỉ số Tham lam & Sợ hãi", callback_data="check_fear_greed")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⭐Chọn chức năng bên dưới⭐:", reply_markup=reply_markup)

# Hàm main
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
        
