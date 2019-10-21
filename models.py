from app import db
import enum
from sqlalchemy import Enum


class Condition(enum.Enum):
    WAIT_LOCATION = 0
    WAIT_REMINDER = 1
    TRACKING = 2


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    text = db.Column(db.Text, nullable=True)
    status = db.Column(Enum(Condition))

    def get_or_create(self, tg_user):
        self.chat_id = getattr(tg_user, 'id')
        user = Users.query.filter_by(chat_id=self.chat_id).first()
        return user if user else self.create(tg_user)

    def set_point(self, lat, lon):
        self.latitude, self.longitude = lat, lon
        if not all([self.latitude, self.longitude]):
            self.status = Condition.WAIT_LOCATION
        else:
            self.status = Condition.WAIT_REMINDER
        db.session.add(self)
        db.session.commit()

    def set_text(self, text):
        self.text = text
        self.status = Condition.TRACKING
        db.session.add(self)
        db.session.commit()

    def create(self, tg_user):
        self.chat_id = getattr(tg_user, 'id')
        self.status = Condition.WAIT_LOCATION
        db.session.add(self)
        db.session.commit()
        return self
