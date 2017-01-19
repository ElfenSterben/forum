

class NOTIFY_TYPE():
    mapping = {
        'announce': '系统消息',
        'remind': '提    醒',
        'message': '私    信'
    }
    ANNOUNCE = 'announce'
    REMIND = 'remind'
    MESSAGE = 'message'

# 消息的目标类型
class TARGET_TYPE():
    COMMENT = 'comment'
    REPLY = 'reply'
    POST = 'post'

# 消息的订阅动作
class ACTION():
    COMMENT = 'comment'
    REPLY = 'reply'

# 消息产生的原因对应的订阅动作
class REASON_ACTION():
    CREATE_POST = ['comment']
    COMMENT_POST = ['reply']
    REPLY_COMMENT = ['reply']
    REPLY_REPLY = ['reply']
