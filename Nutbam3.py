from telegram import Update
from telegram.ext import ContextTypes

async def handle_Nut_bam_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat_id
    message = "Bạn vừa bấm nút số 3 thành công!"

    await context.bot.send_message(chat_id=chat_id, text=message)
