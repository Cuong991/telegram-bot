from telegram import Update
from telegram.ext import ContextTypes

async def handle_button3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id

    # Nội dung bạn muốn gửi khi bấm nút 3
    await context.bot.send_message(
        chat_id=chat_id,
        text="Bạn vừa bấm nút 3!",
        parse_mode="HTML"
    )
