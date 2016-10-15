var inputChange = function(e){
    var input = e.target
    var td = input.closest('td')
    var p_message = $(td).find('.message').first()
    p_message.removeClass('error')
}


var btnSetInfo = function(e){
    var btn = e.target
    var box = $(btn).closest('.form')
    var email = $(box).find('.email').first().val()
    var form = {
        'email': email
    }
    var response = function(r){
        if (r.success){
            alert('修改成功')
            window.location.reload()
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
    api.setInfo(form, response)
}

var btnChangePassword = function(e){
    var btn = e.target
    var box = $(btn).closest('.form')
    var old_pwd = $(box).find('.old-password').first().val()
    var new_pwd = $(box).find('.new-password').first().val()
    var confirm_pwd = $(box).find('.confirm-password').first().val()
    var form = {
        'old-password': old_pwd,
        'new-password': new_pwd,
        'confirm-password': confirm_pwd
    }
    var response = function(r){
        if (r.success){
            alert('修改成功')
            window.location.reload()
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
    api.changePassword(form, response)
}

var bindEvents = function(){
    $('.btn-set-info').on('click', btnSetInfo)
    $('.btn-change-password').on('click', btnChangePassword)
    $('input').on('input', inputChange)
}

var __main = function(){
    bindEvents()
}

$(document).ready(__main)
