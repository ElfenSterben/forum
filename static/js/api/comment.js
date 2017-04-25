api.commentAdd = function(form, callback){
    let url = '/api/comment/add'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}

api.commentReplyView = function(form, callback){
    let url = '/api/comment/' + String(form.commentid) + '/replies'
    api.get(url, form, callback)
}

api.replyAdd = function(form, callback){
    let url = '/api/reply/add'
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}