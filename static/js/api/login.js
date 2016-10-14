api.login = function(form, callback){
    var url = '/api/login'
    api.post(url, form, callback)
}

api.register = function(form, callback){
    var url = '/api/register'
    api.post(url, form, callback)
}
