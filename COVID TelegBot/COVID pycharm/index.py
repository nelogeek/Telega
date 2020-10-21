
import telebot
from telebot import types

import COVID19Py

covid19 = COVID19Py.COVID19()
bot = telebot.Telebot("1148569083:AAH5QVB2oWda-SUPgup01CjMGabjnUaFcC0")



@bot.message_handler(commands=['start'])
def start(message):
    send_mess = f'<b>Привет {message.from_user.first_name}!</b>\nВведите страну'
    bot.send_message(message.chat, id, send_mess, parse_mode='html')


bot.polling(none_stop=True)

#latest = covid19.getLatest()
#location = covid19.getLocationByCountryCode('US')

print(latest, location)
