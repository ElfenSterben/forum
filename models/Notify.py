from . import Model, db, timestamp

class Notify(Model, db.Model):
    __tablename__ = 'notify'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024 * 10))
    type = db.Column(db.String(100))
    target_id = db.Column(db.Integer)
    target_type = db.Column(db.String(100))
    action = db.Column(db.String(100))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user_notify = db.relationship('UserNotify', lazy='dynamic',cascade="delete, delete-orphan", backref='notify')
    created_time = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content')
        self.type = form.get('type')
        self.target_id = form.get('target_id')
        self.target_type = form.get('target_type')
        self.action = form.get('action')
        self.sender_id = form.get('sender_id')
        self.created_time = timestamp()

    @classmethod
    def new(cls, form):
        n = cls(form)
        n.save()
        return n

    @classmethod
    def news(cls, start_time, query):
        return cls.query.filter(
            Notify.created_time>start_time
        ).filter_by(**query).all()
