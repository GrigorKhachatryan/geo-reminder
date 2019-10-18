import telebot
import geopy.distance
from models import Client
import constant


bot = telebot.TeleBot(constant.token)

temporary_storage = {}


@bot.message_handler(commands=['start'])
def create_new_geolocation(message):
    user = Client().get_or_create(tg_user=message.from_user)
    user.set_status(False)
    user.set_point(None, None)
    bot.send_message(message.chat.id, constant.HELLO_MESSAGE.format(message.from_user.first_name))


@bot.message_handler(content_types=['location'])
def location(message):
    lat, long = message.location.latitude, message.location.longitude
    if not all([lat, long]):
        bot.send_message(message.chat.id, "Что-то не так, не могу понять твои координаты")
    user = Client.query.filter_by(chat_id=message.chat.id).first()
    if user.status is False:
        temporary_storage[user.chat_id] = {'latitude': lat, 'longitude': long}
        keyboard = telebot.types.InlineKeyboardMarkup()
        row = []
        for key, val in {'no': 'Отмена', 'yes': "Напоминалка"}.items():
            row.append(telebot.types.InlineKeyboardButton(text=val, callback_data=key))
        keyboard.add(*row)
        bot.send_message(chat_id=message.chat.id, text='Если все верно, то жми на напоминалку!',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['no', 'yes'])
def processing(call):
    user = Client.query.filter_by(chat_id=call.from_user.id).first()
    if call.data == 'yes':
        point = temporary_storage.pop(user.chat_id)
        user.set_point(point.get('latitude'), point.get('longitude'))
        bot.delete_message(call.from_user.id, call.message.message_id)
        bot.send_message(call.from_user.id, 'О чем тебе напомнить?')
    else:
        bot.edit_message_text("Жду новой геопозиции", call.from_user.id, call.message.message_id)


@bot.message_handler(func=lambda message: True)
def reminders(message):
    user = Client.query.filter_by(chat_id=message.from_user.id).first()
    if all([user.latitude, user.longitude]):
        user.set_text(message.text)
        user.set_status(True)
        bot.send_message(message.chat.id, 'Включай трансляцию геопозиции, '
                                          'чтобы я знал, где ты находишься:)')


@bot.edited_message_handler(content_types=['location'])
def geolocation_training(message):
    user = Client.query.filter_by(chat_id=message.chat.id).first()
    if user.status is True:
        lat, long = message.location.latitude, message.location.longitude
        if geopy.distance.geodesic((lat, long), (user.latitude, user.longitude)).m < 100:
            user.set_status(None)
            bot.send_message(message.chat.id, 'Не забудь!!! \n' + user.text.upper())
