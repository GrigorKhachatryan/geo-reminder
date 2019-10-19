from app import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    text = db.Column(db.Text, nullable=True)
    status = db.Column(db.Integer)

    def get_or_create(self, tg_user):
        self.chat_id = getattr(tg_user, 'id')
        user = Client.query.filter_by(chat_id=self.chat_id).first()
        return user if user else self.create(tg_user)

    def set_point(self, lat, lon):
        self.latitude, self.longitude = lat, lon
        db.session.add(self)
        db.session.commit()

    def set_text(self, text):
        self.text = text
        db.session.add(self)
        db.session.commit()

    def set_status(self, status):
        self.status = status
        db.session.commit()

    def create(self, tg_user):
        self.chat_id = getattr(tg_user, 'id')
        db.session.add(self)
        db.session.commit()
        return self

