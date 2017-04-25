
var btnOnUpdatePost = function(e){
    let msgMapping = {
            'title': '.post-title-message',
            'content': '.post-content-message',
            'node_id': '.post-node-message'
        }
    let btn = e.target
    let box = $(btn).closest('.div-post-form')
    let title = $(box).find('.input-post-title').first().val()
    let content = $(box).find('.input-post-content').first().val()
    let node_id = $(box).find('.select-node').first().val()
    let sendData = {
        'title': title,
        'content': content,
        'node_id': node_id
    }
    let response = function(r){
        if (r.success){
                let data = r.data
                window.location.href = data.url
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
    api.postAdd(sendData, response)
}



var bindEvents = function(){
    $('.btn-post-add').on('click', btnOnUpdatePost)
}

var __main = function(){
    bindEvents()
}

$(document).ready(__main)
