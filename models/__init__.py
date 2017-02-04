from flask_sqlalchemy import SQLAlchemy
from flask import url_for
import time


db = SQLAlchemy()

def timestamp():
    return int(time.time())


class Model(object):
    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def hidden(self):
        self.hidden = True
        db.session.commit()

    def _update(self):
        db.session.merge(self)
        db.session.commit()

from services.NotifyService import notify_service
from services.NotifyService import *