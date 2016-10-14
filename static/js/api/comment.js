api.commentAdd = function(form, callback){
    var url = '/api/comment/add'
    api.post(url, form, callback)
}
