api.nodeAdd = function(form, callback){
    var url = '/api/node/add'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.nodeDelete = function(form, callback){
    var url = '/api/node/delete'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}
