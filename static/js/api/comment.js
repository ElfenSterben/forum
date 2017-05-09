api.commentAdd = function(form, callback){
    var url = '/api/comment/add'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.commentReplyView = function(form, callback){
    var url = '/api/comment/' + String(form.commentid) + '/replies'
    api.get(url, form, callback)
}

api.replyAdd = function(form, callback){
    var url = '/api/reply/add'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}