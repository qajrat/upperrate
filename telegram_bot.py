from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time

# Замените 'YOUR_API_TOKEN' на токен, который вы получили от BotFather
API_TOKEN = 'YOUR_API_TOKEN'

# Текст сообщения, на которое бот должен отвечать
TARGET_MESSAGE = "привет"

# Текст ответа
RESPONSE_MESSAGE = "Спасибо!"

# Хранилище для хранения информации о сообщениях
user_messages = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Отправьте мне сообщение "привет", и я буду отвечать на него каждые две минуты.')

def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if update.message.text and update.message.text.lower() == TARGET_MESSAGE:
        # Сохраняем информацию о сообщении
        user_messages[user_id] = {
            'chat_id': update.message.chat_id,
            'message_id': update.message.message_id,
            'last_response_time': time.time()
        }
        update.message.reply_text(RESPONSE_MESSAGE)

def periodic_check(context: CallbackContext):
    current_time = time.time()
    for user_id, message_info in list(user_messages.items()):
        if current_time - message_info['last_response_time'] >= 120:  # 120 секунд = 2 минуты
            context.bot.send_message(chat_id=message_info['chat_id'], text=RESPONSE_MESSAGE)
            user_messages[user_id]['last_response_time'] = current_time

def main():
    # Создаем экземпляр Updater и передаем ему токен вашего бота
    updater = Updater(API_TOKEN, use_context=True)

    # Получаем диспетчер для регистрации обработчиков
    dp = updater.dispatcher

    # Обработчик команды /start
    dp.add_handler(CommandHandler("start", start))

    # Обработчик текстовых сообщений
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск периодической задачи
    job_queue = updater.job_queue
    job_queue.run_repeating(periodic_check, interval=60.0, first=0.0)

    # Запуск бота
    updater.start_polling()

    # Останавливаем бота при нажатии Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()
