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
        un = user.user_notifies.notify