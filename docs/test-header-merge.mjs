import MarkdownIt from 'markdown-it'
import multimd from 'markdown-it-multimd-table'

const md = new MarkdownIt().use(multimd, {
  rowspan: true,
  colspan: true
})

const input = `
| Header 1 | Header 2 |
| --- | --- |
| ^^ | Cell 3 |
`

console.log(md.render(input))
