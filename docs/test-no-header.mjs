import MarkdownIt from 'markdown-it'
import multimd from 'markdown-it-multimd-table'

const md = new MarkdownIt().use(multimd, {
  rowspan: true,
  colspan: true
})

const input = `
|:---|:---|
| R1 C1 | R1 C2 |
| ^^ | R2 C2 |
`

console.log(md.render(input))
