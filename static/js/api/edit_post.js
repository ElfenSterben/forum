api.postAdd = function(form, callback){
    let post_id = $('.div-post-form').data('id')
    let url = '/api/post/update' + '/' + post_id
    let data = JSON.stringify(form)
    api.post(url, data, callback)
}
