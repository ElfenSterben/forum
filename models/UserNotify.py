from . import Model, db, timestamp

class UserNotify(Model, db.Model):
    __tablename__ = 'user_notify'
    id = db.Column(db.Integer, primary_key=True)
    is_read = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    notify_id = db.Column(db.Integer, db.ForeignKey('notify.id', ondelete='CASCADE'))
    created_time = db.Column(db.Integer)

    def __init__(self, form):
        self.user_id = form.get('user_id')
        self.notify_id = form.get('notify_id')
        self.created_time = timestamp()

    @classmethod
    def new(cls, form):
        un = cls(form)
        un.save()
        return un
