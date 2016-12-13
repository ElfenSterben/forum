
var btnOnUpdatePost = function(e){
    var btn = e.target
    var box = $(btn).closest('.div-post-form')
    var title = $(box).find('.input-post-title').first().val()
    var content = $(box).find('.input-post-content').first().val()
    var node_id = $(box).find('.select-node').first().val()
    console.log(node_id)
    var sendData = {
        'title': title,
        'content': content,
        'node_id': node_id
    }
    var response = function(r){
        if (r.success){
                var data = r.data
                var url = base_url + data.url
                window.location.href = url
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

    api.postAdd(sendData, response)
}



var bindEvents = function(){
    $('.btn-post-add').on('click', btnOnUpdatePost)
}

var __main = function(){
    bindEvents()
}

$(document).ready(__main)
