api.setInfo = function(form, callback){
    let url = '/api/user/change/info'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.changePassword = function(form, callback){
    let url = '/api/user/change/password'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.uploadAvatar = function(data, callback){
    let url = '/api/user/upload/avatar'
    api.post(url, data, callback)
}