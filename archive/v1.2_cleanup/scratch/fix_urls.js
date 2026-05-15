const fs = require('fs');

const files = [
  'docs/bg/lektionen/lektion34.md',
  'docs/bg/lektionen/lektion37.md',
  'docs/bg/lektionen/lektion38.md',
  'docs/bg/lektionen/lektion43.md',
  'docs/bg/lektionen/lektion53.md',
  'docs/bg/lektionen/lektion59.md',
  'docs/bg/lektionen/lektion60.md',
  'docs/bg/lektionen/uebung51.md'
];

files.forEach(file => {
  let content = fs.readFileSync(file, 'utf-8');
  content = content.replace(/<(http[^>]+)>/g, '[$1]($1)');
  fs.writeFileSync(file, content);
  console.log(`Fixed URLs in ${file}`);
});
