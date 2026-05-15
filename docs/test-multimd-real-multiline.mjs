import MarkdownIt from 'markdown-it'
import multimd from 'markdown-it-multimd-table'

const md = new MarkdownIt().use(multimd, { multiline: true })

const input = `
| Header |
| :--- |
| Zeile 1
  Zeile 2 |
`

console.log(md.render(input))
