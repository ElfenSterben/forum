api.postAdd = function(form, callback){
    var url = '/api/post/add'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}
