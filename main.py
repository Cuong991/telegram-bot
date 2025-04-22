import os
import requests
from io import BytesIO
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import nest_asyncio
import asyncio

# Token của bạn
TOKEN = "7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk"

# Hàm chụp ảnh và cắt ảnh
def capture_and_crop():
    try:
        # URL cần chụp
        url = "https://coinmarketcap.com/vi/"

        # Gọi API screenshot miễn phí
        screenshot_url = f"https://api.screenshotmachine.com?key=YOUR_SCREENSHOTMACHINE_API_KEY&url={url}&dimension=1024xfull"

        response = requests.get(screenshot_url)
        img = Image.open(BytesIO(response.content))

        # Cắt ảnh (tọa độ cần chỉnh tùy khu vực)
        left = 100
        top = 300
        right = 900
        bottom = 600
        cropped_img = img.crop((left, top, right, bottom))

        # Lưu ảnh tạm
        output = BytesIO()
        cropped_img.save(output, format='PNG')
        output.seek(0)

        return output
    except Exception as e:
        print(f"Lỗi khi chụp và cắt ảnh: {e}")
        return None

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Xem chỉ số Tham lam & Sợ hãi", callback_data="check_fear_greed")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("⭐ Chọn chức năng:", reply_markup=reply_markup)

# Khi bấm nút
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    if query.data == "check_fear_greed":
        photo = capture_and_crop()
        if photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption="Chỉ số Tham lam & Sợ hãi hiện tại là:",
                parse_mode="HTML"
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="Không thể lấy ảnh, vui lòng thử lại sau."
            )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
        
