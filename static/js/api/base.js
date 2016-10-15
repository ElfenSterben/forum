var api = {}
api.ajax = function(url, method, form, callback){
    form = JSON.stringify(form)
    var request = {
        url: url,
        type: method,
        contentType: "application/json; charset=utf-8",
        data: form,
        success: function(response){
            callback(response)
        },
        error: function(err){
            var r = {
                'success': false,
                'message': '网络错误'
            }
            callback(r)
        }
    }
    $.ajax(request)
}

api.post = function(url, form, callback){
    api.ajax(url, 'post', form, callback)
}

api.get = function(url, callback){
    api.ajax(url, 'get', {}, callback)
}

var base_url = 'http://kaede.cc'
