import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram.ext import ContextTypes

# Thay đổi token bot Telegram và OpenAI API key của bạn
TOKEN = '7804124843:AAGIrk9aIOZ9cfjrf0jhsOTZCCUoKHEgHLk'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

# Cấu hình OpenAI API
openai.api_key = OPENAI_API_KEY

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "👋 Xin chào, tôi là GPT AI được huấn luyện bởi @cuong49\n\n"
        "💬 Tôi có thể giúp bạn trả lời các câu hỏi, giải thích, hoặc chỉ đơn giản là trò chuyện với bạn. "
        "Hãy cứ hỏi bất kỳ điều gì bạn muốn, và tôi sẽ cố gắng giúp đỡ bạn! 😄\n\n"
        "✨ Hãy thử hỏi tôi một câu hỏi nào đó nhé!"
    )
    await update.message.reply_text(welcome_message)

# Hàm xử lý tin nhắn người dùng, trả lời bằng OpenAI GPT
async def chat_with_ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text

    # Gửi câu hỏi người dùng đến OpenAI GPT-3
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Hoặc chọn model khác của OpenAI
            prompt=user_message,
            max_tokens=150,
            temperature=0.7
        )
        # Lấy câu trả lời từ OpenAI và gửi lại cho người dùng
        ai_response = response.choices[0].text.strip()
        await update.message.reply_text(ai_response)
    except Exception as e:
        await update.message.reply_text(f"❌ Đã xảy ra lỗi khi xử lý câu hỏi: {e}")

# Hàm chính để chạy bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Đăng ký các handler
    application.add_handler(CommandHandler("start", start))  # Lệnh /start
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_ai))  # Trả lời tin nhắn

    application.run_polling()

if __name__ == "__main__":
    main()
