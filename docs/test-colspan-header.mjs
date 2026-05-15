import MarkdownIt from 'markdown-it'
import multimd from 'markdown-it-multimd-table'

const md = new MarkdownIt().use(multimd, {
  rowspan: true,
  colspan: true
})

const input = `
| Sandhi-Regeln ||
| --- | --- |
| Context 1 | Rule 1 |
| ^^ | Example 1 |
`

console.log(md.render(input))
