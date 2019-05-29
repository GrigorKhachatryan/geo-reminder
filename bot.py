import telebot
import random
import math
from telebot.types import Message
TOKEN = '820420748:AAF77jTIa-47autLICs2m0XXJZ-V2nJNIdk'
bot = telebot.TeleBot(TOKEN)

smiles = ['😘',
          '👍',
          '😂',
          '😂',
          '😒',
          ]

@bot.message_handler(commands=['start'])
def hello_bot(message):
    bot.send_message(message.chat.id, 'Привет, ты можешь указать свою геопозицию и я скажу тебе, сколько до меня метров')

@bot.message_handler(content_types=['location'])
def location(message):
    long = message.location.longitude
    lat = message.location.latitude
    la = 55.688815
    lo = 37.904171
    R = 111138
    x = (long - lo) * math.cos((lat + la) * 0.00872664626)
    y = lat - la
    d = int(R * math.sqrt(x * x + y * y))
    bot.send_message(message.chat.id,f'Расстояние до Гриши: {d} метров')

@bot.message_handler(func=lambda message: True)
def upper(message):
    bot.send_message(message.chat.id, random.choice(smiles))



bot.polling()
