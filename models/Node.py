from . import Model, db, timestamp

class Node(Model, db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.Integer)
    edited_time = db.Column(db.Integer)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(100))
    posts = db.relationship('Post', lazy='dynamic',cascade="delete, delete-orphan", backref='node')
    hidden = db.Column(db.Boolean, default=False)

    def __init__(self, form):
        self.created_time = timestamp()
        self.edited_time = timestamp()
        self.name = form.get('name')
        self.description = form.get('description', '')

    @classmethod
    def new(cls, form):
        node = cls(form)
        node.save()

    @classmethod
    def user_list(cls):
        data = {}
        node_list = Node.query.filter_by(hidden=False)
        data['node_list'] = node_list
        return data

    def json(self):
        r = {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
        return r