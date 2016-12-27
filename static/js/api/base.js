var api = {}
api._ajax = function(url, method, data, contentType, callback){
    var csrfToken = $('meta[name=csrf-token]').attr('content')
    var request = {
        url: url,
        type: method,
        contentType: contentType,
        data: data,
        headers: {'X-CSRFToken': csrfToken},
        success: function(response){
            callback(response)
        },
        error: function(err){
            var r = {
                'success': false,
                'message': {'.message':'网络错误'}
            }
            callback(r)
        }
    }
    $.ajax(request)
}

api.ajax = function(url, method, data, callback){
    var contentType = "application/json; charset=utf-8"
    api._ajax(url, method, data, contentType, callback)
}

api.post = function(url, data, callback){
    api.ajax(url, 'post', data, callback)
}

api.get = function(url, data, callback){
    api.ajax(url, 'get', data, callback)
}


//var base_url = 'http://kaede.cc'
 var base_url = 'http://localhost:3000'
