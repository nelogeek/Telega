import telebot
from telebot import types
import COVID19Py

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot('1123630574:AAHiYybkmYeB7tW7C8KmyJoQrfp76yVTQgM')


@bot.message_handler(content_types=['text'])
def Games(message):
    if message.text == "Блэкджек":

        key = types.InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn = types.KeyboardButton('...')
        bot.send_message(None, f'Запускаю',
                         reply_markup=key)
        BlackJack()


@bot.message_handler(content_types=['text'])
class BlackJack():
    count = 0
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Да')
    btn2 = types.KeyboardButton('Нет')
    keyboard.add(btn1, btn2)
    bot.send_message(f'Будете брать карту?', reply_markup=keyboard)
    part()

    def part():
        if message.text == 'Да':
            count = count + koloda.pop()


# Это нужно чтобы бот работал всё время
bot.polling(none_stop=True)
