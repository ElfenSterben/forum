api.nodeAdd = function(form, callback){
    var url = '/api/node/add'
    api.post(url, form, callback)
}

api.nodeDelete = function(form, callback){
    var url = '/api/node/delete'
    api.post(url, form, callback)
}
