import MarkdownIt from 'markdown-it'
import multimd from 'markdown-it-multimd-table'

const md = new MarkdownIt().use(multimd, {
  multiline: true,
  rowspan: true,
  colspan: true
})

const input = `
| Header 1 | Header 2 |
| :--- | :--- |
| Context | Rule Line 1
            Rule Line 2
            Rule Line 3 |
`

console.log(md.render(input))
