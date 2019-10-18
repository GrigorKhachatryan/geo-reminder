from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from constant import token, URI
import reminder

print(reminder)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/' + token, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = reminder.telebot.types.Update.de_json(json_string)
    reminder.bot.process_new_updates([update])
    return ''


if __name__ == '__main__':
    from models import *
    db.create_all()
    reminder.bot.polling()
