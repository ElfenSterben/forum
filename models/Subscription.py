from . import Model, db, timestamp

class Subscription(Model, db.Model):
    __tablename__ = 'subscription'
    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer)
    target_type = db.Column(db.String(100))
    action = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    created_time = db.Column(db.Integer)

    def __init__(self, form):
        self.target_id = form.get('target_id', '')
        self.target_type = form.get('target_type', '')
        self.action = form.get('action', '')
        self.user_id = form.get('user_id', '')
        self.created_time = timestamp()

    @classmethod
    def new(cls, form):
        s = cls(form)
        s.save()
        return s
