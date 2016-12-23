api.setInfo = function(form, callback){
    var url = '/api/user/change/info'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.changePassword = function(form, callback){
    var url = '/api/user/change/password'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.uploadAvatar = function(data, callback){
    var url = '/api/user/upload/avatar'
    api.post(url, data, callback)
}