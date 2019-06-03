import os

import telebot
import geopy.distance
from database import db,Client
from hello_message import HELLO_MESSAGE
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

temporary_storage = {}
status = ['No']
trecking = [False]

@bot.message_handler(commands=['new'])
def New(message):
    trecking[0] = False
    temporary_storage.clear()
    Client.query.filter_by(id=message.chat.id).delete()
    bot.send_message(message.chat.id, HELLO_MESSAGE.format(message.from_user.first_name))

@bot.message_handler(commands=['start'])
def hello_bot(message):
    bot.send_message(message.chat.id, HELLO_MESSAGE.format(message.from_user.first_name))


@bot.message_handler(content_types=['location'])
def location(message):
    if trecking[0] == False:
        long = message.location.longitude
        lat = message.location.latitude
        temporary_storage.update({'latitude': lat, 'longitude': long, 'id': message.chat.id})
        keyboard = telebot.types.InlineKeyboardMarkup()
        row = []
        for key, val in {'no': 'Отмена', 'yes': "Напоминалка"}.items():
            row.append(telebot.types.InlineKeyboardButton(text=val, callback_data=key))
        keyboard.add(*row)
        bot.send_message(chat_id=message.chat.id, text='Если все верно, то жми на напоминалку!', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in ['no', 'yes'])
def processing(call):
    if call.data == 'yes' and temporary_storage != {}:

        status[0] = 'Ok'
        trecking[0] = True

        bot.delete_message(call.from_user.id, call.message.message_id)

        bot.send_message(call.from_user.id, 'О чем тебе напомнить?')
    else:
        status[0] = 'No'
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.from_user.id, 'Жду твоей новой геопозиции')

@bot.message_handler(func=lambda message: True)
def reminders(message):
    if status[0] == 'Ok':
        status[0] = 'No'
        trecking[0] = True
        trecking.append(message.date)
        temporary_storage.update({'text': message.text})
        result = Client(id=temporary_storage['id'], longitude=temporary_storage['longitude'], latitude=temporary_storage['latitude'], text=temporary_storage['text'])
        reminder_admin = Client.query.filter_by(id=temporary_storage['id']).first()
        if reminder_admin == None:
            db.session.add(result)
        else:
            reminder_admin.longitude = temporary_storage['longitude']
            reminder_admin.latitude = temporary_storage['latitude']
            reminder_admin.text = temporary_storage['text']
        db.session.commit()


        bot.send_message(message.chat.id, 'Включай трансляцию геопозиции, чтобы я знал, где ты находишься:)')

@bot.edited_message_handler(content_types=['location'])
def location(message):
    if  Client.query.filter_by(id=message.chat.id).first() != None:
        reminder = Client.query.filter_by(id=message.chat.id).first()
        lat = message.location.latitude
        long = message.location.longitude
        if geopy.distance.geodesic((lat, long), (reminder.latitude, reminder.longitude)).m < 5000:
            Client.query.filter_by(id=message.chat.id).delete()
            bot.send_message(message.chat.id, 'Не забудь!!! \n' + reminder.text.upper())
            bot.send_message(244027971, 'Приехал')




bot.polling()
