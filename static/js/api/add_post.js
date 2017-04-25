api.postAdd = function(form, callback){
    let url = '/api/post/add'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}
