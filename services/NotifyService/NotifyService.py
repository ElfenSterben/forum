from models.Notify import Notify
from models.UserNotify import UserNotify
from models.Subscription import Subscription
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
        last_announce = user.last_user_notify(NOTIFY_TYPE.ANNOUNCE)
        last_time = last_announce.notify.created_time if last_announce is not None else 0

        query = {
            'type': NOTIFY_TYPE.ANNOUNCE
        }
        ns = Notify.news(last_time, query)

        for n in ns:
            data = {
                'user_id': user.id,
                'notify_id': n.id
            }
            UserNotify.new(data)

    def pull_remind(self, user):
        subscriptions = user.get_subscriptions()
        last_remind = user.last_user_notify(NOTIFY_TYPE.REMIND)
        last_time = last_remind.notify.created_time if last_remind is not None else 0

        notifies = []
        for s in subscriptions:
            _time = last_time if last_time > s.created_time else s.created_time
            query ={
                'type' : NOTIFY_TYPE.REMIND,
                'target_id':s.target_id,
                'target_type' : s.target_type,
                'action' : s.action
            }
            n = Notify.news(_time, query)
            notifies.extend(n)

        notifies.sort(key=lambda n: n.created_time)

        for n in notifies:
            data = {
                'user_id': user.id,
                'notify_id': n.id
            }
            UserNotify.new(data)

    def subscribe(self, user, target_id, target_type, reason):
        for a in reason:
            data = {
                'target_id': target_id,
                'target_type': target_type,
                'action': a,
                'user_id': user.id,
            }
            Subscription.new(data)

    def cancel_subscribe(self, user, target_id, target_type, reason):
        for a in reason:
            ss = user.subscriptions.filter_by(target_id=target_id, target_type=target_type, action=a)
            ss.delete()

    def get_subscription_config(self, user):
        return user.subscription_config.json()

    def update_subscription_config(self, user, form):
        try:
            sc = user.subscription_config
            sc.update(form)
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_notifies(self, user):
        uns = user.user_notifies.order_by(UserNotify.created_time.desc())
        return uns

    def read(self, user_notifies):
        for un in user_notifies:
            un.is_read = True
            un._update()
