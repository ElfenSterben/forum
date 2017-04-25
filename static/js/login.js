var animationRegister ={
    left: '70px'
}

var animationLogin = {
    left: '0px'
}

var onSelected = function(e){
    let animationSelect = {
        '.login-view': animationLogin,
        '.register-view': animationRegister
    }
    let div = e.target
    let data = $(div).data('selected')
    let animation = animationSelect[data]
    $('.bottom-line').stop()
    $('.bottom-line').animate(animation, 500, 'swing')
    $('.view-item').addClass('hidden')
    $(data).removeClass('hidden')
}


var btnOnLogin = function(e){
    let btn = e.target
    let box = $(btn).closest('.login-view')
    let username = $(box).find('.username').first().val()
    let password = $(box).find('.password').first().val()
    let form = {
        'username': username,
        'password': password
    }
    let response = function(r){
        if (r.success){
            window.location.href = r.referrer
        }
        else{
            let message = r.message
            for (let k in message){
                let p_message = $(box).find(k).first()
                p_message.text(message[k])
                p_message.addClass('error')
            }

        }
    }
    api.login(form, response)
}


var btnOnRegister = function(e){
    let btn = e.target
    let view = $(btn).closest('.register-view')
    let username = $(view).find('.username').first().val()
    let password = $(view).find('.password').first().val()
    let confirm = $(view).find('.confirm-password').first().val()
    let email = $(view).find('.email').first().val()

    let form = {
        'username': username,
        'password': password,
        'confirm': confirm,
        'email': email
    }
    let response = function(r){
        if (r.success){
            window.location.href = r.referrer
        }
        else{
            let message = r.message
            for (let k in message){
                let p_message = $(view).find(k).first()
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
