import MarkdownIt from 'markdown-it'
import gridtables from 'markdown-it-gridtables'

const md = new MarkdownIt().use(gridtables.default || gridtables)

const input = `
+---+---+
| a | b |
+   +---+
|   | c |
+---+---+
`

console.log(md.render(input))
