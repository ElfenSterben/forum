
var formatTime = function(current_time, old_time){
        var timestamp = current_time - old_time
        var seconds = timestamp
        var minutes = parseInt(seconds/60)
        var hours = parseInt(minutes/60)
        var day = parseInt(hours/24)
        var formattedTime = ''
        if (day != 0){
            if (day <= 30){
                formattedTime = day + "天前"
            }
            else{
                formattedTime = new Date(old_time * 1000).toLocaleString()
            }
        }
        else if(hours > 0){
            formattedTime = hours + "小时前"
        }
        else if(minutes > 0){
            formattedTime = minutes + "分钟前"
        }
        else{
            formattedTime = "刚刚"
        }
        return formattedTime
    }

var resetTime = function(){
    var current_time = $('div.timestamp').first().text()
    var usr_reg_time = $('time.usr-reg-time').first()
    var reg_time = parseInt(usr_reg_time.text())
    usr_reg_time.text(new Date(reg_time * 1000).toLocaleString())
    var time = $('time:not(.usr-reg-time)')
    var length = time.length
    time.each(function(){
        $(this).text(formatTime(current_time, $(this).text()))
        })
}


var __main = function(){
    resetTime()
}

$(document).ready(__main)
