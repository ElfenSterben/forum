api.postAdd = function(form, callback){
    var url = '/api/post/add'
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}
api.postUpdate = function(form, callback){
    var post_id = $('.div-post-form').data('id')
    var url = '/api/post/update' + '/' + post_id
    var data = JSON.stringify(form)
    api.post(url, data, callback)
}

