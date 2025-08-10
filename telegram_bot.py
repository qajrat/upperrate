from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import asyncio
import time

# Замените 'YOUR_API_TOKEN' на токен, который вы получили от BotFather
API_TOKEN = '8473543376:AAEyqXRUnPP3WNY0KbhHcYsZY_-3whCJmkA'

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
    if update.message.text.lower() == TARGET_MESSAGE:
        # Сохраняем информацию о сообщении
        user_messages[user_id] = {
            'chat_id': update.message.chat_id,
            'message_id': update.message.message_id,
            'last_response_time': time.time()
        }
        update.message.reply_text(RESPONSE_MESSAGE)

async def periodic_check(bot: Bot):
    while True:
        current_time = time.time()
        for user_id, message_info in list(user_messages.items()):
            if current_time - message_info['last_response_time'] >= 120:  # 120 секунд = 2 минуты
                await bot.send_message(chat_id=message_info['chat_id'], text=RESPONSE_MESSAGE)
                user_messages[user_id]['last_response_time'] = current_time
        await asyncio.sleep(60)  # Проверяем каждую минуту

def main():
    bot = Bot(token=API_TOKEN)
    updater = Updater(bot=bot, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Запуск асинхронной задачи для периодической проверки
    loop = asyncio.get_event_loop()
    loop.create_task(periodic_check(bot))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
