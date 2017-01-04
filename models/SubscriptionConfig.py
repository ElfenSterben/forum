from . import Model, db, timestamp

class SubscriptionConfig(Model, db.Model):
    __tablename__ = 'subscription_config'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    comment = db.Column(db.Boolean, default=True)
    reply = db.Column(db.Boolean, default=True)

    def __init__(self, form):
        self.user_id = form.get('user_id', '')

    @classmethod
    def new(cls, form):
        sc = cls(form)
        sc.save()
        return sc
