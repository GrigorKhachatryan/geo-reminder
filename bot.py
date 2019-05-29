import telebot
import random
import geopy.distance
TOKEN = '820420748:AAF77jTIa-47autLICs2m0XXJZ-V2nJNIdk'
bot = telebot.TeleBot(TOKEN)

smiles = ['😘',
          '👍',
          '😂',
          '😂',
          '😒',
          ]

temporary_storage = {}

@bot.message_handler(commands=['start'])
def hello_bot(message):
    bot.send_message(message.chat.id, 'Привет, ты можешь указать свою геопозицию и я скажу тебе, сколько до меня метров')

@bot.message_handler(content_types=['location'])
def location(message):
    long = message.location.longitude
    lat = message.location.latitude
    # dist = int(geopy.distance.geodesic((lat, long), (la, lo)).m)
    temporary_storage[message.chat.id] = {'lat': lat ,'long': long}
    keyboard = telebot.types.InlineKeyboardMarkup()
    row = []
    for key, val in {'no': 'Отмена', 'yes': "Напоминалка"}.items():
        row.append(telebot.types.InlineKeyboardButton(text=val, callback_data=key))
    keyboard.add(*row)
    bot.send_message(chat_id=message.chat.id, text='Если все верно, то жми на напоминалку!', reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def upper(message):
    bot.send_message(message.chat.id, f'Расстояние до Гриши: {temporary_storage} метров')
    print(message)

@bot.edited_message_handler(content_types=['location'])
def location(message):
    long = message.location.longitude
    lat = message.location.latitude
    la = 55.688815
    lo = 37.904171
    dist = int(geopy.distance.geodesic((lat, long), (la, lo)).m)
    bot.send_message(message.chat.id, f'Расстояние до Гриши: {dist} метров')

bot.polling()
