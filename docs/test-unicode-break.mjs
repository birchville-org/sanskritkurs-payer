import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({ breaks: true })

const input = 'Line 1\u2028Line 2'

console.log(md.render(input))
