

class NOTIFY_TYPE():
    ANNOUNCE = 'announce'
    REMIND = 'remind'
    MESSAGE = 'message'

# 消息的目标类型
class TARGET_TYPE():
    COMMENT = '评论'
    REPLY = '回复'
    POST = '文章'

# 消息的订阅动作
class ACTION():
    COMMENT = '评论'
    REPLY = '回复'

# 消息产生的原因对应的订阅动作
class REASON_ACTION():
    CREATE_POST = ['comment']
    COMMENT_POST = ['reply']
    REPLY_COMMENT = ['reply']
    REPLY_REPLY = ['reply']
