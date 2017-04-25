var nodeTemplate = function(n){
    let n = `
    <div class="node-box">
        <div class="node-item" data-id="${n.id}">
            <div class="node-title">
                <h1>${n.name}</h1>
            </div>
            <div class="node-content">
                ${n.description}
            </div>
            <div class="node-action">
                <button class="node-delete" type="button">删除</button>
            </div>
        </div>
    </div>
    `
    return n
}

var btnOnNewNode = function(e){
    let btn = e.target
    let box = $(btn).closest('.node-input-box')
    let name = $(box).find('.input-node-content').first().val()
    let description = $(box).find('.input-node-description').first().val()
    let form = {
        'name': name,
        'description': description
    }
    let response = function(r){
        if (r.success){
            n = r.data
            $('.node-lists').prepend(nodeTemplate(n))
        }
        else{
            alert(r.message)
        }
    }
    api.nodeAdd(form, response)
}

var btnOnDeleteNode = function(e){
    let btn = e.target
    let item = $(btn).closest('.node-item')
    let box = $(item).closest('.node-box')
    let id = $(item).data('id')
    let form = {
        'id': id
    }
    let response = function(r){
        if (r.success){
            box.remove()
            alert('删除成功')
        }
        else{
            alert(r.message)
        }
    }
    api.nodeDelete(form, response)
}

var bindEvents = function(){
    $('.node-new').on('click', btnOnNewNode)
    $('.node-lists').on('click', '.node-delete', btnOnDeleteNode)
}

var __main = function(){
    bindEvents()
}

$(document).ready(__main);
