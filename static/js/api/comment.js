api.commentAdd = function(form, callback){
    var url = '/api/comment/add'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}
