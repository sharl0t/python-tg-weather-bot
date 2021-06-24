import telebot
from telebot import types
import pyowm  # Импортируем пакет с помощью которого мы узнаем погоду
# import os  # Импортируем для использования переменных окружения
import time
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'  # your language here, eg. Portuguese
owm = OWM('3a67c5c3b5d76d479a049e2fc8de64b4', config_dict)
bot = telebot.TeleBot('1843880588:AAF6uS0suEMV1hdfPIkisDaFaWV4i2mdxOU')

@bot.message_handler(content_types=['text'])
def send_message(message):
    if message.text.lower() == "/start" or message.text.lower() == "/help":
        bot.send_message(message.from_user.id, "Здравствуйте. Вы можете узнать здесь погоду. Просто напишите название города." + "\n")
    else:
        try:
            mgr = owm.weather_manager()
            observation = mgr.weather_at_place(message.text)  # the observation object is a box containing a weather object
            weather = observation.weather
            temp = weather.temperature("celsius")["temp"]  # Присваиваем переменной значение температуры из таблицы
            temp = round(temp)
            veter = weather.wind()['speed']
           # Формируем и выводим ответ
            print(time.ctime(), "UID:", message.from_user.id, "Сообщение:", message.text.title(), "Температура:", temp)
            answer = f"В городе " + message.text + " сейчас " + str(weather.detailed_status) + "." + "\n"
            answer += f"Температура около: " + str(temp) + " С." + "\n"
            answer += f'Скорость ветра примерно: ' + str(veter) + 'м\c.' + '\n'
            if veter <= 0.2:
                answer += f'На улице нет ветра.'
            if veter > 0.2 and veter <= 1.5:
                answer += f'На улице тихий ветер.'
            if veter > 1.5 and veter <= 6:
                answer += f'На улице легкий ветер.'
            if veter > 6 and veter <= 10:
                answer += f'На улице слабый ветер.'
            if veter > 11 and veter <= 16:
                answer += f'На улице крепкий ветер.'
            if veter > 16 and veter <= 30:
                answer += f'На улице очень сильный ветер, буря.'
        except Exception:
            answer = "Не найден город, попробуйте ввести название снова.\n"
            print(time.ctime(), "UID:", message.from_user.id, "Сообщение:", message.text.title(), '!Ошибка!')
        bot.send_message(message.chat.id, answer)  # Ответить сообщением


# Запускаем бота
bot.polling(none_stop=True)
