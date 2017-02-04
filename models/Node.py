from . import Model, db

class Node(Model, db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100))
    posts = db.relationship('Post', lazy='dynamic',cascade="delete, delete-orphan", backref='node')
    hidden = db.Column(db.Boolean, default=False)

    def __init__(self, form):
        self.name = form.get('name')
        self.description = form.get('description', '')

    @classmethod
    def new(cls, form):
        node = cls(form)
        node.save()

    def json(self):
        r = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return r