api.login = function(form, callback){
    var url = '/api/login'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.register = function(form, callback){
    var url = '/api/register'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}
