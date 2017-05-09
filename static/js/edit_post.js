
var btnOnUpdatePost = function(e){
    var msgMapping = {
            'title': '.post-title-message',
            'content': '.post-content-message',
            'node_id': '.post-node-message'
        }
    var btn = e.target
    var box = $(btn).closest('.div-post-form')
    var title = $(box).find('.input-post-title').first().val()
    var content = $(box).find('.input-post-content').first().val()
    var node_id = $(box).find('.select-node').first().val()
    var sendData = {
        'title': title,
        'content': content,
        'node_id': node_id
    }
    var response = function(r){
        if (r.success){
            var data = r.data
            window.location.href = data.url
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
    api.postAdd(sendData, response)
}

var editPostBindEvents = function(){
    $('.btn-post-add').on('click', btnOnUpdatePost)
}

var __main = function(){
    editPostBindEvents()
}

$(document).ready(__main)
