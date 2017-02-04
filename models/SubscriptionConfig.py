from . import Model, db, timestamp

class SubscriptionConfig(Model, db.Model):
    __tablename__ = 'subscription_config'
    # id = db.Column(db.Integer,)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id',ondelete='CASCADE'), primary_key=True, unique=True)
    comment = db.Column(db.Boolean, default=True)
    reply = db.Column(db.Boolean, default=True)

    def __init__(self):
        pass

    def update(self, form):
        self.comment = form.get('comment', True)
        self.reply = form.get('reply', True)
        self._update()

    def json(self):
        data = {
            'comment': self.comment,
            'reply': self.reply
        }
        return data