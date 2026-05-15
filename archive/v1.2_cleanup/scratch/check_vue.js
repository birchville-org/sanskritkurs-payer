const fs = require('fs');
const path = require('path');
const compiler = require('@vue/compiler-dom');

const files = ['docs/bg/lektionen/lektion21.md', 'docs/bg/lektionen/uebung38.md'];

for (const file of files) {
  const content = fs.readFileSync(file, 'utf-8');
  try {
    const parsed = compiler.parse(content);
    if (parsed.errors && parsed.errors.length > 0) {
      console.log(`Error in ${file}:`);
      parsed.errors.forEach(e => console.log(`  - ${e.message} at line ${e.loc.start.line}`));
    } else {
      console.log(`SUCCESS: ${file}`);
    }
  } catch (err) {
    console.log(`Crash in ${file}: ${err.message}`);
  }
}
