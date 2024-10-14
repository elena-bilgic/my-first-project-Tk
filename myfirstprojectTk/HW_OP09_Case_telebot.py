import telebot
import random
import time
import schedule
import threading


#API_token granted by Telegram:
#7912743208:AAEluUXLW9t7EqdzLHN58k9cVvLW15q1Ypw

bot = telebot.TeleBot( '7912743208:AAEluUXLW9t7EqdzLHN58k9cVvLW15q1Ypw')

# Хранилище для фотографий пользователя
user_data = {}


def generate_outfits(tops, bottoms, shoes):
    outfits = []
    for day in range(7):
        top = random.choice(tops)
        bottom = random.choice(bottoms)
        shoe = random.choice(shoes)
        outfits.append(f"День {day + 1}: {top}, {bottom}, {shoe}")
    return outfits


def send_daily_outfit(chat_id):
    user = user_data.get(chat_id)
    if user and 'outfits' in user:
        today_outfit = user['outfits'].pop(0)
        bot.send_message(chat_id, f"Доброе утро! Сегодняшний наряд: {today_outfit}")


def request_new_photos(chat_id):
    bot.send_message(chat_id,
                     "Пора обновить ваш гардероб! Пожалуйста, пришлите мне фото минимум 3 топов, 3 брюк или юбок и минимум 2 пары обуви.")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'tops': [], 'bottoms': [], 'shoes': [], 'outfits': []}
    bot.send_message(chat_id, "Приветствую! Давайте составим ваш капсульный гардероб. Пришлите мне фото топов.")


@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    chat_id = message.chat.id
    user = user_data.get(chat_id)

    if not user:
        bot.send_message(chat_id, "Пожалуйста, начните с команды /start.")
        return

    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    if len(user['tops']) < 3:
        user['tops'].append(file_path)
        bot.send_message(chat_id, f"Топ добавлен. Всего топов: {len(user['tops'])}")
        if len(user['tops']) == 3:
            bot.send_message(chat_id, "Теперь пришлите фото брюк или юбок.")
    elif len(user['bottoms']) < 3:
        user['bottoms'].append(file_path)
        bot.send_message(chat_id, f"Низ добавлен. Всего низов: {len(user['bottoms'])}")
        if len(user['bottoms']) == 3:
            bot.send_message(chat_id, "Теперь пришлите фото обуви.")
    elif len(user['shoes']) < 2:
        user['shoes'].append(file_path)
        bot.send_message(chat_id, f"Обувь добавлена. Всего обуви: {len(user['shoes'])}")
        if len(user['shoes']) == 2:
            bot.send_message(chat_id, "Спасибо! Ваш гардероб готов. Буду присылать вам наряды каждый день.")
        user['outfits'] = generate_outfits(user['tops'], user['bottoms'], user['shoes'])

# Планировщик задач для ежедневной отправки нарядов и запроса новых фото
def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


def setup_schedule():
    for chat_id in user_data.keys():
        schedule.every().day.at("08:00").do(send_daily_outfit, chat_id=chat_id)
        schedule.every().sunday.at("20:00").do(request_new_photos, chat_id=chat_id)

if __name__ == "__main__":
    setup_schedule()
    threading.Thread(target=schedule_checker).start()

bot.polling(none_stop=True)
