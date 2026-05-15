import MarkdownIt from 'markdown-it'
import multimd from 'markdown-it-multimd-table'

const md = new MarkdownIt({ breaks: true }).use(multimd)

const input = `
| Header |
| :--- |
| Line 1 \\
  Line 2 |
`

console.log(md.render(input))
