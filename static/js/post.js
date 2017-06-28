
var commentTemplate = function(d){
    var c = d.comment
    var u = d.user
    c.content = c.content.replace(/</g, '&lt;')
    c.content = c.content.replace(/>/g, '&gt;')

    var t = `
    <div id="id-comment-${c.id}" class="comment-item inner-box" data-commentid="${c.id}">
            <div class="comment-body clear-fix">
                <div class="comment-user-avatar float-left">
                    <img class="img-middle" src="${u.avatar}" alt="" />
                </div>
                <div class="comment-item-right float-left">
                    <div class="comment-user-name">
                        <a class="my-link" href="${u.url}">${u.username}</a>
                        <time>${c.created_time}</time>
                    </div>
                    <div class="comment-comment">
                        <span>${c.content}</span>
                    </div>
                </div>
            </div>
            <div class="comment-action clear-fix">
                <p class="reply-view-message"></p>
                <a class="my-link btn-reply-view not-view float-right">展开回复</a>
            </div>
            <div class="reply-view hidden">
                <div class='reply-container'>
                </div>
                <div class="reply-pages">
                    <div class="center">
                    </div>
                </div>
            </div>
        </div>
    `
    return t
}

var replyTemplate = function(d){
    var reply = d.reply
    var sender = d.sender
    var receiver = d.receiver
    var recContent = ``
    if (receiver !== null){
        recContent = `
        回复&nbsp;<a class="my-link" href="${receiver.url}"> ${receiver.username}</a>:
        `
    }

    reply.content = reply.content.replace(/</g, '&lt;')
    reply.content = reply.content.replace(/>/g, '&gt;')
    var t = `
    <div class="reply-item" data-replyid="${reply.id}">
        <div class="reply-item-left">
            <div class="reply-sender-avatar">
                <img class="img-small" src="${sender.avatar}">
            </div>
            <div class="reply-sender-name">
                <a class="my-link" href="${sender.url}}}">${sender.username}</a>
            </div>
        </div>
        <div class="reply-item-right">
            <div class="reply-content">
                <p>${recContent}${reply.content}</p>
            </div>
        </div>
        <div class="reply-item-foot"><a class="reply-this my-link">回复</a></div>
    </div>
    `
    return t
}

var btnOnNewComment = function(e){
    var msgMapping = {
        'content': '.comment-message',
        'post_id': '.comment-message',
    }
    var btn = e.target
    var box = $(btn).closest('.comment-input-body')
    var message = $('.comment-message').first()
    var list = $('.comment-list').first()
    var content = $('.input-comment').first().val()
    var postID = $('.input-comment').first().data('postid')
    var form = {
        'content': content,
        'post_id': postID
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
                var c = msgMapping[k]
                var p_message = $(box).find(c).first()
                p_message.text(message[k][0])
                p_message.addClass('error')
            }
        }
    }
    api.commentAdd(form, response)
}

var repliesTemplete = function(data){
    var replies = data.reply_list
    var templetes = ``
    for(var i=0; i<replies.length; i++ ){
        var t = replyTemplate(replies[i])
        templetes += t
    }
    console.log(templetes)
    return templetes
}   

var replyPagesTemplete = function(data){
    var currentPage = data.current_page
    var pages = data.pages
    var prePageEnable = ''
    var nextPageEnable = ''
    if(currentPage <= 1){
        prePageEnable = 'disabled'
    }
    if(currentPage >= pages){
        nextPageEnable = 'disabled'
    }
    var prePageBtn = `
        <button class="reply-page-button reply-page" ${prePageEnable} data-page="${currentPage-1}" >上一页</button>
    `
    var nextPageBtn = `
        <button class="reply-page-button reply-page" ${nextPageEnable} data-page="${currentPage+1}">下一页</button>
    `
    var t = ``
    for (var i=1; i<=pages; i++){
        if (currentPage === i){
            t += `<button class="reply-page-button">${i}</button>`
        }
        else{
            t +=`<button class="reply-page-button reply-page" data-page="${i}">${i}</button>`
        }
    }
    t = prePageBtn + t + nextPageBtn
    return t
}

var insertIntoReplyView = function(replyView, data){
    var repliesTemp = repliesTemplete(data)
    var pagesTemp = replyPagesTemplete(data)
    $(replyView).find('.reply-container').html(repliesTemp) 
    $(replyView).find('.reply-pages div').html(pagesTemp)
}

var btnOnPageReplies = function(e){
    var btn = e.target
    var commentItem = $(btn).closest('.comment-item')
    var replyView = $(commentItem).find('.reply-view')
    var commentID = $(commentItem).data('commentid')
    var page = $(btn).data('page')
    var form = {
        'commentid': commentID,
        'page':page,
    }
    var response = function(r){
        if (r.success){
                var data = r.data
                insertIntoReplyView(replyView, data)
        }
        else{
            var message = r.message
            for (var k in message){
                var pMessage = $(commentItem).find(k).first()
                pMessage.text(message[k])
                pMessage.addClass('error')
            }
        }
    }
    api.commentReplyView(form, response)
}

var btnOnViewReplies = function(e){
    var btn = e.target
    $(btn).toggleClass('not-view')
    var item = $(btn).closest('.comment-item')
    var replyView = $(item).find('.reply-view')
    var viewHidden = $(replyView).is(":hidden")
    $(replyView).stop()
    $(replyView).slideToggle()
    if (viewHidden){
        $(replyView).addClass('viewed')
        btnOnPageReplies(e)
    }
}

var btnOnNewReply = function(e){
    var btn = e.target
    var box = $(btn).closest('.reply-view')
    var divInput = $(btn).closest('.div-reply-input')
    var replyID = $(divInput).data('replyid')
    var message = $('.reply-message').first()
    var container = $(box).find('.reply-container').first()
    var content = $(box).find('.input-reply').first().val()
    var commentID = $(box).find('.input-reply').first().data('commentid')
    var receiverName = ''
    if(content.startsWith('回复') && content.includes(':')){
        receiverName = content.split('回复 ')[1].split(':')[0]
    }
    var form = {
        'reply_id': replyID,
        'comment_id': commentID,
        'content': content,
        'receiver_name': receiverName,
    }
    var response = function(r){
        if (r.success){
                var data = r.data
                console.log(data)
                var t = replyTemplate(data)
                container.append(t)
        }
        else{
            var message = r.message
            for (var k in message){
                var p_message = $(box).find('.reply-message').first()
                p_message.text(message[k])
                p_message.addClass('error')
            }
        }
    }
    api.replyAdd(form, response)
}

var btnOnReplySomeOne = function(e) {
    var btn = e.target
    var box = $(btn).closest('.reply-view')
    var item = $(btn).closest('.reply-item')
    var senderName = $(item).find('.reply-sender-name a').first().text()
    var input = $(box).find('textarea.input-reply')
    var replyID = $(item).data('replyid')
    var text = '回复 ' + senderName + ':'
    $(box).find('.div-reply-input').data('replyid', replyID)
    input.val(text)
    input.focus()
}

var remarkContent = function() {
    var settings = {
        html: false,
        xhtmlOut: false,
        breaks: false,
        langPrefix: 'language-',
        linkTarget: 'blank',
        typographer: true,
        highlight: (str, lang) => {
            if (!window.hljs) {
                return '';
            }
            var hljs = window.hljs;
            if (lang && hljs.getLanguage(lang.toLowerCase())) {
                try {
                    return hljs.highlight(lang.toLowerCase(), str).value;
                } catch (__) {
                }
            }
            try {
                return hljs.highlightAuto(str).value;
            } catch (__) {
            }
            return ''
        }
    }
    var md = new Remarkable('full', settings)
    var input = e('.post-body')
    var source = input.innerHTML.trim()
    var textarea = document.createElement('textarea')
    textarea.innerHTML = source
    var view = md.render(textarea.value)
    input.innerHTML = view
}

var commentBindEvents = function() {
    $('.btn-new-comment').on('click', btnOnNewComment)
    $('.comment-list').on('click', '.btn-reply-view', btnOnViewReplies)
    $('.comment-list').on('click', '.reply-page', btnOnPageReplies)
    $('.comment-list').on('click', '.btn-new-reply', btnOnNewReply)
    $('.reply-view').on('click', '.reply-this', btnOnReplySomeOne)
}

var __main = function(){
    commentBindEvents()
    remarkContent()
}

$(document).ready(__main)
