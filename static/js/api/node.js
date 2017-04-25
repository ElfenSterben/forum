api.nodeAdd = function(form, callback){
    let url = '/api/node/add'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.nodeDelete = function(form, callback){
    let url = '/api/node/delete'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}
