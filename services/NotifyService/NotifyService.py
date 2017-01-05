from models.Notify import Notify
from models.UserNotify import UserNotify
from .NotifyConfig import *

class NotifyService(object):

    def create_announce(self, content, sender_id):
        data = {
            'content': content,
            'sender_id': sender_id,
            'type': NOTIFY_TYPE.ANNOUNCE,
        }
        Notify.new(data)

    def create_remind(self, target_id, target_type, action, sender_id, content):
        data = {
            'target_id': target_id,
            'target_type': target_type,
            'action': action,
            'sender_id': sender_id,
            'content': content,
            'type': NOTIFY_TYPE.REMIND,
        }
        Notify.new(data)

    def create_message(self, content, sender_id, receiver_id):
        data = {
            'content': content,
            'sender_id': sender_id,
            'type': NOTIFY_TYPE.MESSAGE,
        }
        n = Notify.new(data)
        data = {
            'user_id': receiver_id,
            'notify_id': n.id,
        }

        UserNotify.new(data)

    def pull_announce(self, user):
        last_announce = user.user_notifies.notify.filter_by(type=NOTIFY_TYPE.ANNOUNCE).last()
        if last_announce is not None:
            last_time = last_announce.created_time
            announce = Notify.query.filter_by(type=NOTIFY_TYPE.ANNOUNCE)
            ns = announce.filter('created_time>:created_time').params(created_time=last_time).all()
            for n in ns:
                data = {
                    'user_id': user.id,
                    'notify_id': n.id
                }
                UserNotify.new(data)

    def pull_remind(self, user):
        subscriptions = user.subscriptions
        for s in subscriptions:
            n = Notify.query.filter_by(target_id=s.target_id, target_type=s.target_type, action=s.action).filter('created_time>:created_time').params(created_time=s.created_time)