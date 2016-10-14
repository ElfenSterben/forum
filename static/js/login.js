var animationRegister ={
    left: '70px'
}

var animationLogin = {
    left: '0px'
}

var onSelected = function(e){
    var animationSelect = {
        '.login-view': animationLogin,
        '.register-view': animationRegister
    }
    var div = e.target
    var data = $(div).data('selected')
    var animation = animationSelect[data]
    $('.bottom-line').stop()
    $('.bottom-line').animate(animation, 500, 'swing')
    $('.view-item').addClass('hidden')
    $(data).removeClass('hidden')
}


var btnOnLogin = function(e){
    var btn = e.target
    var box = $(btn).closest('.login-view')
    var username = $(box).find('.username').first().val()
    var password = $(box).find('.password').first().val()
    var form = {
        'username': username,
        'password': password
    }
    var response = function(r){
        if (r.success){
            var url = base_url
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
    api.login(form, response)
}


var btnOnRegister = function(e){
    var btn = e.target
    var view = $(btn).closest('.register-view')
    var username = $(view).find('.username').first().val()
    var password = $(view).find('.password').first().val()
    var confirm = $(view).find('.confirm-password').first().val()
    var email = $(view).find('.email').first().val()

    var form = {
        'username': username,
        'password': password,
        'confirm': confirm,
        'email': email
    }
    var response = function(r){
        if (r.success){
            var url = base_url
            window.location.href = url
        }
        else{
            var message = r.message
            for (var k in message){
                var p_message = $(view).find(k).first()
                p_message.text(message[k])
                p_message.addClass('error')
            }
        }
    }
    api.register(form, response)
}


var bindEvent = function(){
    $('.check-item').on('click', onSelected)
    $('.btn-login').on('click', btnOnLogin)
    $('.btn-register').on('click', btnOnRegister)
}

var __main = function(){
    bindEvent()
}


$(document).ready(__main)
