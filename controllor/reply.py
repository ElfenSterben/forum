from forms.ReplySchema import reply_schema
from forms.UserSchema import user_schema
from models.Reply import Reply
from services.NotifyService import notify_service, TARGET_TYPE, REASON_TYPE, ACTION_TYPE


def add(form):
    result = dict(success=False)
    res = reply_schema.load(form)
    if res.errors == {}:
        result['success'] = True
        r = Reply.new(res.data)
        data = dict(
            reply=reply_schema.dump(r),
            sender=user_schema.dump(r.sender),
            receiver=None
        )
        if r.receiver is not None:
            data['receiver'] = user_schema.dump(r.receiver)
            create_notify_with_receiver(form.get('reply_id'), r)
        else:
            create_notify_without_receiver(r)
        subscribe_reply(r)
        result['data'] = data
    result['message'] = res.errors
    return result

def subscribe_reply(reply):
    subscribe = {
        'user': reply.sender,
        'target_id': reply.id,
        'target_type': TARGET_TYPE.REPLY,
        'reason': REASON_TYPE.REPLY_COMMENT
    }
    notify_service.subscribe(**subscribe)

def create_notify_with_receiver(target_id, reply):
    notify = {
        'target_id': target_id,
        'target_type': TARGET_TYPE.REPLY,
        'action': ACTION_TYPE.REPLY,
        'sender_id': reply.sender_id,
        'content': reply.sender.username + '在' + reply.comment.post.title + '回复了你',
    }
    notify_service.create_remind(**notify)

def create_notify_without_receiver(reply):
    notify = {
        'target_id': reply.comment_id,
        'target_type': TARGET_TYPE.COMMENT,
        'action': ACTION_TYPE.REPLY,
        'sender_id': reply.sender_id,
        'content': reply.sender.username + '在' + reply.comment.post.title + '回复了你',
    }
    notify_service.create_remind(**notify)
