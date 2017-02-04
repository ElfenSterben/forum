var inputChange = function(e){
    var input = e.target
    var td = input.closest('td')
    var p_message = $(td).find('.message').first()
    console.log(p_message)
    p_message.remove()
}

var fileChange = function(e){
    var input = e.target
    $('#selected-img').cropper('replace', URL.createObjectURL(input.files[0]))
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
    $('input').on('input', inputChange)
    $('.file-input').on('change', fileChange)
    $('.btn-set-info').on('click', btnSetInfo)
    $('.btn-change-password').on('click', btnChangePassword)
}

var initCrop = function(){
    img_x = $('#data-img-x')
    img_y = $('#data-img-y')
    img_nw = $('#data-img-nw')
    img_nh = $('#data-img-nh')
    $('#selected-img').cropper({
        dragMode: 'move',
        aspectRatio: 1/1,
        viewMode: 1,
        preview: '.img-preview',
        minContainerWidth: 200,
        minContainerHeight: 200,
        cropBoxMovable: false,
        cropBoxResizable: false,
        toggleDragModeOnDblclick: false,
        crop: function(e) {
        // Output the result data for cropping image.
        img_x.val(Math.round(e.x))
        img_y.val(Math.round(e.y))
        img_nw.val(Math.round(e.width))
        img_nh.val(Math.round(e.height))
      }
    });
}

var __main = function(){
    bindEvents()
    initCrop()
}

$(document).ready(__main)
