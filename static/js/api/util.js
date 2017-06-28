var log = console.log.bind(console)

var e = selector => {
    return document.querySelector(selector)
}
var es = selector => {
    return document.querySelectorAll(selector)
}
var bindEvent = (selector, action, callback) => {
    var self = e(selector)
    self.addEventListener(action, callback)
}

var elementBindEvent = (element, action, callback) => {
    element.addEventListener(action, callback)
}

var appendHTML = (element, html) => {
    element.insertAdjacentHTML('beforeEnd', html)
}

var find = (element, selector) => {
    return element.querySelector(selector)
}

var findAll = (element, selector) => {
    return element.querySelectorAll(selector)
}

var inserToCursor = (field, value) => {
    var curValue = field.value
    var startPos = field.selectionStart
    var endPos = field.selectionEnd
    var restoreTop = field.scrollTop
    var newValue = curValue.substring(0, startPos) + value + curValue.substring(endPos, curValue.length)
    field.value = newValue
    if (restoreTop > 0) {
        field.scrollTop = restoreTop;
    }
    field.focus()
    field.selectionStart = startPos + value.length;
    field.selectionEnd = startPos + value.length;
}
