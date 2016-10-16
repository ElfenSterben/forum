var commentTemplate = function(d){
    var c = d.comment
    var u = d.user
    c.content = c.content.replace(/</g, '&lt;')
    c.content = c.content.replace(/>/g, '&gt;')
    var t = `
    <div class="comment-item inner-box clearfix">
        <div class="comment-user-avatar float-left">
            <img class="img-middle" src="${u.avatar}" alt="" />
        </div>
        <div class="comment-item-right float-left">
            <div class="comment-user-name">
                <a class="my-link" href="/user/${u.username}">${u.username}</a>
                <span>${c.created_time}</span>
            </div>
            <div class="comment-comment">
                <span>${c.content}</span>
            </div>
        </div>
    </div>
    `
    return t
}

var btnOnNewComment = function(e){
    var btn = e.target
    var box = $(btn).closest('.comment-input-body')
    var message = $('.comment-message').first()
    var list = $('.comment-list').first()
    var content = $('.input-comment').first().val()
    var post_id = $('.input-comment').first().data('postid')
    var form = {
        'content': content,
        'post_id': post_id
    }
    message.text('')
    var response = function(r){
        if (r.success){
                var data = r.data
                var t = commentTemplate(data)
                list.append(t)
        }
        else{
            var message = r.message
            for (var k in message){
                var p_message = $(box).find(k).first()
                p_message.text(message[k])
                p_message.addClass('error')
            }
        }
    }
    api.commentAdd(form, response)
}

var bindEvents = function(){
    $('.btn-new-comment').on('click', btnOnNewComment)
}

var __main = function(){
    bindEvents()
}

$(document).ready(__main)
