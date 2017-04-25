api.login = function(form, callback){
    let url = '/api/login'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.register = function(form, callback){
    let url = '/api/register'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}
