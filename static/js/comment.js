
var commentTemplate = function(d){
    let c = d.comment
    let u = d.user
    c.content = c.content.replace(/</g, '&lt;')
    c.content = c.content.replace(/>/g, '&gt;')

    let t = `
    <div id="id-comment-${c.id}" class="comment-item inner-box" data-commentid="${c.id}">
            <div class="comment-body clearfix">
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
            <div class="comment-action clearfix">
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
    let reply = d.reply
    let sender = d.sender
    let receiver = d.receiver
    let recContent = ``
    if (receiver !== null){
        recContent = `
        回复&nbsp;<a class="my-link" href="${receiver.url}"> ${receiver.username}</a>:
        `
    }

    reply.content = reply.content.replace(/</g, '&lt;')
    reply.content = reply.content.replace(/>/g, '&gt;')
    let t = `
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
    let msgMapping = {
        'content': '.comment-message',
        'post_id': '.comment-message',
    }
    let btn = e.target
    let box = $(btn).closest('.comment-input-body')
    let message = $('.comment-message').first()
    let list = $('.comment-list').first()
    let content = $('.input-comment').first().val()
    let postID = $('.input-comment').first().data('postid')
    let form = {
        'content': content,
        'post_id': postID
    }
    message.text('')
    let response = function(r){
        if (r.success){
                let data = r.data
                let t = commentTemplate(data)
                list.append(t)
        }
        else{
            let message = r.message
            for (let k in message){
                let c = msgMapping[k]
                let p_message = $(box).find(c).first()
                p_message.text(message[k][0])
                p_message.addClass('error')
            }
        }
    }
    api.commentAdd(form, response)
}

var repliesTemplete = function(data){
    
    let replies = data.reply_list
    
    let templetes = ``
    for(let i=0; i<replies.length; i++ ){
        let t = replyTemplate(replies[i])
        templetes += t
    }
    console.log(templetes)
    return templetes
}   

var replyPagesTemplete = function(data){
    let currentPage = data.current_page
    let pages = data.pages
    let prePageEnable = ''
    let nextPageEnable = ''
    if(currentPage <= 1){
        prePageEnable = 'disabled'
    }
    if(currentPage >= pages){
        nextPageEnable = 'disabled'
    }
    let prePageBtn = `
        <button class="reply-page-button reply-page" ${prePageEnable} data-page="${currentPage-1}" >上一页</button>
    `
    let nextPageBtn = `
        <button class="reply-page-button reply-page" ${nextPageEnable} data-page="${currentPage+1}">下一页</button>
    `
    let t = ``
    for (let i=1; i<=pages; i++){
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
    let repliesTemp = repliesTemplete(data)
    let pagesTemp = replyPagesTemplete(data)
    $(replyView).find('.reply-container').html(repliesTemp) 
    $(replyView).find('.reply-pages div').html(pagesTemp)
}

var btnOnPageReplies = function(e){
    let btn = e.target
    let commentItem = $(btn).closest('.comment-item')
    let replyView = $(commentItem).find('.reply-view')
    let commentID = $(commentItem).data('commentid')
    let page = $(btn).data('page')
    let form = {
        'commentid': commentID,
        'page':page,
    }
    let response = function(r){
        if (r.success){
                let data = r.data
                insertIntoReplyView(replyView, data)
        }
        else{
            let message = r.message
            for (let k in message){
                let pMessage = $(commentItem).find(k).first()
                pMessage.text(message[k])
                pMessage.addClass('error')
            }
        }
    }
    api.commentReplyView(form, response)
}

var btnOnViewReplies = function(e){
    let btn = e.target
    $(btn).toggleClass('not-view')
    let item = $(btn).closest('.comment-item')
    let replyView = $(item).find('.reply-view')
    let viewHidden = $(replyView).is(":hidden")
    $(replyView).stop()
    $(replyView).slideToggle()
    if (viewHidden){
        $(replyView).addClass('viewed')
        btnOnPageReplies(e)
    }
}

var btnOnNewReply = function(e){
    let btn = e.target
    let box = $(btn).closest('.reply-view')
    let divInput = $(btn).closest('.div-reply-input')
    let replyID = $(divInput).data('replyid')
    let message = $('.reply-message').first()
    let container = $(box).find('.reply-container').first()
    let content = $(box).find('.input-reply').first().val()
    let commentID = $(box).find('.input-reply').first().data('commentid')
    let receiverName = ''
    if(content.startsWith('回复') && content.includes(':')){
        receiverName = content.split('回复 ')[1].split(':')[0]
    }
    let form = {
        'reply_id': replyID,
        'comment_id': commentID,
        'content': content,
        'receiver_name': receiverName,
    }
    let response = function(r){
        if (r.success){
                let data = r.data
                console.log(data)
                let t = replyTemplate(data)
                container.append(t)
        }
        else{
            let message = r.message
            for (let k in message){
                let p_message = $(box).find('.reply-message').first()
                p_message.text(message[k])
                p_message.addClass('error')
            }
        }
    }
    api.replyAdd(form, response)
}

var btnOnReplySomeOne = function(e){
    let btn = e.target
    let box = $(btn).closest('.reply-view')
    let item = $(btn).closest('.reply-item')
    let senderName = $(item).find('.reply-sender-name a').first().text()
    let input = $(box).find('textarea.input-reply')
    let replyID = $(item).data('replyid')
    let text = '回复 ' + senderName + ':'
    $(box).find('.div-reply-input').data('replyid', replyID)
    input.val(text)
    input.focus()
}

var bindEvents = function(){
    $('.btn-new-comment').on('click', btnOnNewComment)
    $('.comment-list').on('click', '.btn-reply-view', btnOnViewReplies)
    $('.comment-list').on('click', '.reply-page', btnOnPageReplies)
    $('.comment-list').on('click', '.btn-new-reply', btnOnNewReply)
    $('.reply-view').on('click', '.reply-this', btnOnReplySomeOne)
}

var __main = function(){
    bindEvents()
}

$(document).ready(__main)
