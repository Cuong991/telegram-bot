from html2image import Html2Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import io
import os

TOKEN = "7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk"

async def capture_chart():
    hti = Html2Image()
    save_path = 'chart.png'
    
    try:
        # Screenshot full trang
        hti.screenshot(
            url='https://coinmarketcap.com/vi/charts/fear-and-greed-index/',
            save_as=save_path,
            size=(1200, 900)  # Kích thước màn hình
        )
        
        if not os.path.exists(save_path):
            raise Exception("Không tạo được file ảnh!")

        with open(save_path, 'rb') as f:
            return io.BytesIO(f.read())
    except Exception as e:
        print("Capture error:", e)
        return None

async def send_chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    photo = await capture_chart()
    if photo:
        await context.bot.send_photo(chat_id=chat_id, photo=photo, caption="Chỉ số tham lam và sợ hãi hiện tại:")
    else:
        await context.bot.send_message(chat_id=chat_id, text="Xin lỗi, không thể lấy chỉ số lúc này!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Xem chỉ số tham lam và sợ hãi", callback_data='fear_greed')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Chọn một chức năng:', reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'fear_greed':
        await send_chart(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
        
