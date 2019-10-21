from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from reminder import *
from constant import TOKEN, URI


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''


def start_on_server():
    bot.set_webhook(url='https://georeminder.herokuapp.com/' + TOKEN)
    app.run(host='0.0.0.0', port=5432, debug=True)


if __name__ == '__main__':
    from models import *
    db.create_all()
    bot.pilling()
