from services.NotifyService import(
    notify_service,
    TARGET_TYPE,
    REASON_TYPE,
    ACTION_TYPE
)
from models.Comment import Comment
from models.Post import Post
from forms.CommentSchema import comment_schema
from forms.UserSchema import user_schema

def add(form):
    result = dict(success=False)
    res = comment_schema.load(form)
    if res.errors == {}:
        result['success'] = True
        c = Comment.new(res.data)
        user = c.user
        data = dict(
            comment=comment_schema.dump(c).data,
            user=user_schema.dump(user).data
        )
        result['data'] = data
        create_notify(c.post, user)
        subscribe_comment(c, user)
    result['message'] = res.errors
    return result

def form_valid(form):
    result = dict(
        valid=False,
        msg=dict()
    )
    p = Post.query.get(form.get('post_id'))
    valid_post_exist = p is not None
    content = form.get('content', '')
    content = content.strip()
    valid_content_len = 200 >= len(content) >= 1
    message = result['msg']
    if not valid_post_exist:
        message['.comment-message'] = '主题不存在'
    elif not valid_content_len:
        message['.comment-message'] = '内容不能为空'
    result['valid'] = valid_post_exist  and valid_content_len
    return result

def create_notify(post, sender):
    notify = {
        'target_id': post.id,
        'target_type': TARGET_TYPE.POST,
        'action': ACTION_TYPE.COMMENT,
        'sender_id': sender.id,
        'content': sender.username + '评论了你的文章' + post.title,
    }
    user_link = '<a href="{}">{}</a>'
    notify_service.create_remind(**notify)

def subscribe_comment(comment, user):
    subscribe = {
        'user': user,
        'target_id': comment.id,
        'target_type': TARGET_TYPE.COMMENT,
        'reason': REASON_TYPE.COMMENT_POST
    }
    notify_service.subscribe(**subscribe)