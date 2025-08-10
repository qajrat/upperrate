from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import time

# Замените 'YOUR_API_TOKEN' на токен, который вы получили от BotFather
API_TOKEN = '8473543376:AAEyqXRUnPP3WNY0KbhHcYsZY_-3whCJmkA'

# Текст сообщения, на которое бот должен отвечать
TARGET_MESSAGE = "привет"

# Текст ответа
RESPONSE_MESSAGE = "Спасибо!"

# Хранилище для хранения информации о сообщениях
user_messages = {}

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Привет! Отправьте мне сообщение "привет", и я буду отвечать на него каждые две минуты.')

async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if update.message.text and update.message.text.lower() == TARGET_MESSAGE:
        # Сохраняем информацию о сообщении
        user_messages[user_id] = {
            'chat_id': update.message.chat_id,
            'message_id': update.message.message_id,
            'last_response_time': time.time()
        }
        await update.message.reply_text(RESPONSE_MESSAGE)

async def periodic_check(context: CallbackContext):
    current_time = time.time()
    for user_id, message_info in list(user_messages.items()):
        if current_time - message_info['last_response_time'] >= 120:  # 120 секунд = 2 минуты
            await context.bot.send_message(chat_id=message_info['chat_id'], text=RESPONSE_MESSAGE)
            user_messages[user_id]['last_response_time'] = current_time

def main():
    # Создаем экземпляр Application и передаем ему токен вашего бота
    application = Application.builder().token(API_TOKEN).build()

    # Обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск периодической задачи
    application.job_queue.run_repeating(periodic_check, interval=60.0, first=0.0)

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
