

var btnOnNewPost = function(e, editor){
    var msgMapping = {
        'title': '.post-title-message',
        'content': '.post-content-message',
        'node_id': '.post-node-message'
    }
    var btn = e.target
    var box = $(btn).closest('.div-post-form')
    var title = $(box).find('.input-post-title').first().val()
    var content = editor.txt.html() //$(box).find('.input-post-content').first().val()
    var node_id = $(box).find('.select-node').first().val()
    log(node_id)
    var sendData = {
        'title': title,
        'content': content,
        'node_id': node_id
    }
    var response = function(r){
        if (r.success){
                var data = r.data
                window.location.href = data.url
        }
        else{
            var message = r.message
            for (var k in message){
                var c = msgMapping[k]
                var p_message = $(box).find(c).first()
                p_message.text(message[k][0])
                p_message.addClass('error')
            }
        }
    }
    api.postAdd(sendData, response)
}

var addPostBindEvents = function(editor){
    $('.btn-post-add').on('click', event => {
        btnOnNewPost(event, editor)
    })
}

var createEditor = () => {
    var E = window.wangEditor
    var editor = new E('#id-div-editor-toolbar', '#id-div-editor-input')
    var menus = [
        'head',  // 标题
        'bold',  // 粗体
        'italic',  // 斜体
        'underline',  // 下划线
        'strikeThrough',  // 删除线
        'foreColor',  // 文字颜色
        'backColor',  // 背景颜色
        'link',  // 插入链接
        'list',  // 列表
        'justify',  // 对齐方式
        'quote',  // 引用
        'image',  // 插入图片
        'table',  // 表格
        'video',  // 插入视频
        'code',  // 插入代码
        'undo',  // 撤销
        'redo'  // 重复
    ]
    editor.customConfig.menus = menus
    editor.create()
    return editor
}

var __main = function(){
    var editor = createEditor()
    addPostBindEvents(editor)

}

$(document).ready(__main)
