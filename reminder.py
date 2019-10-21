import telebot
from geopy import distance
from models import Users, Condition
from constant import TOKEN, HELLO_MESSAGE


bot = telebot.TeleBot(TOKEN)

temporary_storage = {}


@bot.message_handler(commands=['start'])
def create_new_geolocation(message):
    user = Users().get_or_create(tg_user=message.from_user)
    if all([user.latitude, user.longitude]):
        user.set_point(None, None)
    bot.send_message(message.chat.id, HELLO_MESSAGE.format(message.from_user.first_name))


@bot.message_handler(content_types=['location'])
def location(message):
    lat, lon = message.location.latitude, message.location.longitude
    if not all([lat, lon]):
        bot.send_message(message.chat.id, "Что-то не так, не могу понять твои координаты")
        return

    user = Users.query.filter_by(chat_id=message.chat.id).first()
    if user.status != Condition.WAIT_LOCATION:
        return

    temporary_storage[user.chat_id] = {'latitude': lat, 'longitude': lon}
    keyboard = telebot.types.InlineKeyboardMarkup()
    row = []
    for key, val in {'no': 'Отмена', 'yes': "Напоминалка"}.items():
        row.append(telebot.types.InlineKeyboardButton(text=val, callback_data=key))
    keyboard.add(*row)
    bot.send_message(chat_id=message.chat.id, text='Если все верно, то жми на напоминалку!',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['no', 'yes'])
def processing(call):
    if call.data == 'no':
        bot.edit_message_text("Жду новой геопозиции", call.from_user.id, call.message.message_id)
        return

    user = Users.query.filter_by(chat_id=call.from_user.id).first()
    point = temporary_storage.pop(user.chat_id)
    user.set_point(point.get('latitude'), point.get('longitude'))
    bot.delete_message(call.from_user.id, call.message.message_id)
    bot.send_message(call.from_user.id, 'О чем тебе напомнить?')


@bot.message_handler(func=lambda message: True)
def reminders(message):
    user = Users.query.filter_by(chat_id=message.from_user.id).first()
    if user.status == Condition.WAIT_REMINDER:
        user.set_text(message.text)
        bot.send_message(message.chat.id, 'Включай трансляцию геопозиции, '
                                          'чтобы я знал, где ты находишься:)')


@bot.edited_message_handler(content_types=['location'])
def geolocation_tracking(message):
    user = Users.query.filter_by(chat_id=message.chat.id).first()
    if user.status != Condition.TRACKING:
        return

    lat, lon = message.location.latitude, message.location.longitude
    if distance.geodesic((lat, lon), (user.latitude, user.longitude)).m < 500:
        user.set_point(None, None)
        bot.send_message(message.chat.id, 'Не забудь!!! \n' + user.text.upper())
