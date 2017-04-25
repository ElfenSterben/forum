var api = {}
api._ajax = function(url, method, data, contentType, callback){
    let csrfToken = $('meta[name=csrf-token]').attr('content')
    let request = {
        url: url,
        type: method,
        contentType: contentType,
        data: data,
        headers: {'X-CSRFToken': csrfToken},
        success: function(response){
            callback(response)
        },
        error: function(err){
            let r = {
                'success': false,
                'message': {'.message':'网络错误'}
            }
            callback(r)
        }
    }
    $.ajax(request)
}

api.ajax = function(url, method, data, callback){
    let contentType = "application/json; charset=utf-8"
    api._ajax(url, method, data, contentType, callback)
}

api.post = function(url, data, callback){
    api.ajax(url, 'post', data, callback)
}

api.get = function(url, data, callback){
    api.ajax(url, 'get', data, callback)
}

 var base_url = '/'
