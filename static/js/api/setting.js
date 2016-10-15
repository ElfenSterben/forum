api.setInfo = function(form, callback){
    var url = '/api/user/change/info'
    api.post(url, form, callback)
}

api.changePassword = function(form, callback){
    var url = '/api/user/change/password'
    api.post(url, form, callback)
}
