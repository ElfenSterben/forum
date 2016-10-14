from . import Model, db


class Topic(Model, db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Ingeter, primary_key=True)
    name = db.Column(db.String(30))
    nodes = db.relationship('Node', backref='topic')
    posts = db.relationship('Post', backref='topic')

    def __init__(self, form):
        self.name = form.get('name')