
__all__ = [
    'NOTIFY_TYPE',
    'TARGET_TYPE',
    'ACTION_TYPE',
    'REASON_TYPE'
]

class notify_type():
    def __init__(self):
        self.ANNOUNCE = 'announce'
        self.REMIND = 'remind'
        self.MESSAGE = 'message'
        self.list = self._list()

    def _list(self):
        l = list(self.__dict__.values())
        l.sort()
        return l

    def name(self, type):
        mapping = {
            'announce': '系统消息',
            'remind': '提    醒',
            'message': '私    信'
        }
        return mapping.get(type)

# 消息的目标类型
class target_type():
    def __init__(self):
        self.COMMENT = 'comment'
        self.REPLY = 'reply'
        self.POST = 'post'

# 消息的订阅动作
class action_type():
    def __init__(self):
        self.COMMENT = 'comment'
        self.REPLY = 'reply'

# 消息产生的原因对应的订阅动作
class reason_type():
    def __init__(self):
        self.CREATE_POST = ['comment']
        self.COMMENT_POST = ['reply']
        self.REPLY_COMMENT = ['reply']
        self.REPLY_REPLY = ['reply']

NOTIFY_TYPE = notify_type()
TARGET_TYPE = target_type()
ACTION_TYPE = action_type()
REASON_TYPE = reason_type()

