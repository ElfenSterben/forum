from models.Notify import Notify
from models.UserNotify import UserNotify
from models.Subscription import Subscription
from models.SubscriptionConfig import SubscriptionConfig
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
        user_notifies = user.user_notifies.order_by(UserNotify.created_time.desc()).all()
        last_announce = None
        for un in user_notifies:
            if un.notify.type==NOTIFY_TYPE.ANNOUNCE:
                last_announce = un.notify

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
        ss = user.subscriptions
        subscriptions = []
        for s in ss:
            if getattr(user.subscription_config, s.action) is True:
                subscriptions.append(s)

        notifies = []
        for s in subscriptions:
            print('pull_remind')
            n = Notify.query.filter(Notify.created_time>s.created_time).filter_by( type=NOTIFY_TYPE.REMIND, target_id=s.target_id, target_type=s.target_type, action=s.action).all()
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
            ss = Subscription.query.filter_by(user_id=user.id, target_id=target_id, target_type=target_type, action=a)
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

