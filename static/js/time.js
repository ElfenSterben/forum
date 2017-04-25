
var formatTime = function(current_time, old_time){
        let timestamp = current_time - old_time
        let seconds = timestamp
        let minutes = parseInt(seconds/60)
        let hours = parseInt(minutes/60)
        let day = parseInt(hours/24)
        let formattedTime = ''
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
    let current_time = $('div.timestamp').first().text()
    let usr_reg_time = $('time.usr-reg-time').first()
    let reg_time = parseInt(usr_reg_time.text())
    usr_reg_time.text(new Date(reg_time * 1000).toLocaleString())
    let time = $('time:not(.usr-reg-time)')
    let length = time.length
    time.each(function(){
        $(this).text(formatTime(current_time, $(this).text()))
        })
}


var __main = function(){
    resetTime()
}

$(document).ready(__main)
