class ESMarkDown {
    constructor(selector, settings={}) {
        this.mdInit(settings)
        this._selector = selector
        var box = e(selector)
        this.rawContent = box.innerHTML.trim()
        box.innerHTML = ''
        this.scrollMap = null
        this.onInputChange = (event) => {
            var input = this.input
            var preview = this.preview
            var value = this.md.render(input.value)
            preview.innerHTML = value
            this.scrollMap = null
        }
        this.syncScroll = (event) => {
            var textarea = this.input
            var style = getComputedStyle(textarea)
            var lh = parseFloat(style.lineHeight)
            var lineNo = Math.floor(textarea.scrollTop / lh)
            if (this.scrollMap === null) {
                this.scrollMap = this.createScrollMap()
            }
            var pos = this.scrollMap[lineNo]
            var preview = this.preview
            if (pos === undefined) {
                pos = preview.scrollHeight
            }
            if(window.JQuery != undefined) {
                $(preview).stop(true).animate({
                    scrollTop: pos
                })
            } else {
                preview.scrollTop = pos
            }

        }
    }
    initOptions(settings) {
        settings.html = false
        settings.xhtmlOut = false
        settings.typographer = true
        settings.breaks = false
        settings.langPrefix = 'language-'
        settings.linkTarget = 'blank'
        settings.highlight = (str, lang) => {
            if (!window.hljs) { return ''; }
            var hljs = window.hljs;
            if (lang && hljs.getLanguage(lang.toLowerCase())) {
                try {
                    return hljs.highlight(lang.toLowerCase(), str).value;
                } catch (__) {}
            }
            try {
                return hljs.highlightAuto(str).value;
            } catch (__) {}
            return ''
        }
    }
    mdInit(settings) {
        this.initOptions(settings)
        var md = new Remarkable('full', settings)
        md.inline.ruler.enable(['sup', 'sub', 'ins', 'mark' ]);
        md.renderer.rules.table_open = () => {
            return '<table class="table table-striped">\n';
        }
        md.renderer.rules.paragraph_open = function (tokens, idx) {
            if (tokens[idx].lines && tokens[idx].level === 0) {
                var line = tokens[idx].lines[0]
                return '<p class="line" data-line="' + line + '">'
            }
            return '<p>'
        }
        md.renderer.rules.heading_open = function (tokens, idx) {
            if (tokens[idx].lines && tokens[idx].level === 0) {
                var line = tokens[idx].lines[0]
                return '<h' + tokens[idx].hLevel + ' class="line" data-line="' + line + '">'
            }
            return '<h' + tokens[idx].hLevel + '>'
        }
        this.md = md
    }

    initMenu(box) {

    }

    initInputarea(box) {
        var tmp = `
            <div class="editor-input-area">
                <div class="eidtor-input">
                    <textarea class="editor-textarea editor-box editor-font" name="content"></textarea>
                </div>
                <div class="editor-preview editor-box editor-font markdown">
                </div>
            </div>
        `
        appendHTML(box, tmp)
        this.input = find(box, '.editor-textarea')
        this.preview = find(box, '.editor-preview')
    }

    initTemplete(selector) {
        var box = e(selector)
        box.classList.add('es-markdown-editor')
        this.initInputarea(box)
    }

    tempSourceDiv(textarea) {
        var div = document.createElement('div')
        var style = getComputedStyle(textarea)
        var css = {
            position: 'absolute',
            visibility: 'hidden',
            height: 'auto',
            width: textarea.clientWidth,
            'font-size': style.fontSize,
            'font-family': style.fontFamily,
            'line-height': style.lineHeight,
            'white-space': style.whiteSpace,
        }
        for (let k in css) {
            div.style[k] = css[k]
        }
        return div
    }

    linesNumMap() {
        var textarea = this.input
        var lines = textarea.value.split('\n')
        var sourceLikeDiv = this.tempSourceDiv(textarea)
        var body = e('body')
        body.append(sourceLikeDiv)
        var result = [0]
        var acc = 0
        for (let l of lines) {
            if(l.length == 0){
                acc++
            } else {
                sourceLikeDiv.innerText = l
                var style = getComputedStyle(sourceLikeDiv)
                var h = parseFloat(style.height)
                var lh = parseFloat(style.lineHeight)
                acc += Math.round(h / lh)
            }
            result.push(acc)
        }
        sourceLikeDiv.remove()
        return result
    }

    createScrollMap() {
        var preview = this.preview
        var textarea = this.input
        var style = getComputedStyle(textarea)
        var lh = parseFloat(style.lineHeight)
        var lineNo = Math.floor(textarea.scrollTop / lh)
        var offect = preview.offsetTop
        var lum = this.linesNumMap()
        var sumLines = lum[lum.length - 1]
        var _scrollMap = new Array(sumLines).fill(-1)
        var noEmptyList = [0]
        _scrollMap[0] = 0
        var eLines = findAll(preview, '.line')
        eLines.forEach(function (el, n) {
            var t = el.dataset.line
            if(t === '') {
                return
            }
            t = parseInt(t)
            t = lum[t]
            if(t !== 0) {
                noEmptyList.push(t)
                _scrollMap[t] = Math.round(el.offsetTop - offect)
            }
        })
        noEmptyList.push(sumLines)
        var pos = 0
        _scrollMap[sumLines] = preview.scrollHeight
        for (let i = 1; i < sumLines; i++) {
            if(_scrollMap[i] !== -1) {
                pos++
                continue
            }
            var a = noEmptyList[pos]
            var b = noEmptyList[pos+ 1]
            _scrollMap[i] = Math.round((_scrollMap[b] * (i - a)+ _scrollMap[a] * (b - i)) / (b - a))
        }
        var devLength = lineNo - _scrollMap.length
        var offect = _scrollMap.length - 1
        for (let i = 0; i < devLength; i++) {
            var min = _scrollMap[sumLines - 2]
            var max = preview.scrollHeight
            var avg = (max - min) / devLength
            _scrollMap[offect + i] = min + avg * i
        }
        return _scrollMap
    }

    onTabClick(event) {
        var self = event.target
        var code = event.code
        if(code.toLowerCase() === 'tab') {
            inserToCursor(self, '    ')
            event.preventDefault()
        }
    }

    initSyncScroll() {
        this.scrollMap = this.createScrollMap()
    }

    bindEvents() {
        elementBindEvent(this.input, 'scroll', this.syncScroll)
        elementBindEvent(this.input, 'input', this.onInputChange)
        elementBindEvent(this.input, 'keydown', this.onTabClick)
    }

    initContent() {
        var input = this.input
        input.innerHTML = this.rawContent
        this.preview.innerHTML = this.md.render(input.value)
    }

    mark() {
        var input = this.input
        this.preview.innerHTML = this.md.render(input.value)
        this.initSyncScroll()
    }

    create() {
        var selector = this._selector
        this.initTemplete(selector)
        this.initContent()
        this.initSyncScroll()
        this.bindEvents()
    }
}
