from app import db
import enum
from sqlalchemy import Enum


class MyStatusEnum(enum.Enum):
    WAIT_LOCATION = 0
    WAIT_REMINDER = 1
    TRACKING = 2


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    text = db.Column(db.Text, nullable=True)
    status = db.Column(Enum(MyStatusEnum))

    def get_or_create(self, tg_user):
        self.chat_id = getattr(tg_user, 'id')
        user = Client.query.filter_by(chat_id=self.chat_id).first()
        return user if user else self.create(tg_user)

    def set_point(self, lat, lon):
        self.latitude, self.longitude = lat, lon
        if not all([self.latitude, self.longitude]):
            self.text = None
            self.status = MyStatusEnum.WAIT_LOCATION
        else:
            self.status = MyStatusEnum.WAIT_REMINDER
        db.session.add(self)
        db.session.commit()

    def set_text(self, text):
        self.text = text
        self.status = MyStatusEnum.TRACKING
        db.session.add(self)
        db.session.commit()

    def set_status(self, status):
        self.status = status
        db.session.commit()

    def create(self, tg_user):
        self.chat_id = getattr(tg_user, 'id')
        self.status = MyStatusEnum.WAIT_LOCATION
        db.session.add(self)
        db.session.commit()
        return self
