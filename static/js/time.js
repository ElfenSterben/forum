
var formattime = function(current_time){
    var time = $('time')
    time.map(function(){
        var old_time = $(this).text()
        var timestamp = current_time - old_time
        var seconds = timestamp
        var minutes = parseInt(seconds/60)
        var hours = parseInt(minutes/60)
        var day = parseInt(hours/24)
        if (day != 0){
            if (day <= 30){
                $(this).text(day + "天前")
            }
            else{
                $(this).text(new Date(old_time).toLocaleString())
            }
        }
        else if(hours != 0){
            $(this).text(hours + "小时前")
        }
        else if(minutes != 0){
            $(this).text(minutes + "分钟前")
        }
        else{
            $(this).text(seconds + "秒前")
        }
    })
}

var resettime = function(){
    var current_time = parseInt(Date.parse(new Date()) % 1000)
    var response = function(r){
        if(r.success){
            current_time = r.data.current_time
            formattime(current_time)
        }
    }
    api.getTime(response)
}


$(document).ready(resettime)
