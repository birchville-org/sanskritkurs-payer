const fs = require('fs');
const path = require('path');
const compiler = require('@vue/compiler-dom');

const brokenFiles = [];

function walkDir(dir) {
  const files = fs.readdirSync(dir);
  for (const file of files) {
    const fullPath = path.join(dir, file);
    if (fs.statSync(fullPath).isDirectory()) {
      walkDir(fullPath);
    } else if (fullPath.endsWith('.md')) {
      const content = fs.readFileSync(fullPath, 'utf-8');
      try {
        const parsed = compiler.parse(content);
        if (parsed.errors && parsed.errors.length > 0) {
          brokenFiles.push(fullPath);
        }
      } catch (err) {
        brokenFiles.push(fullPath);
      }
    }
  }
}

walkDir('docs/bg');

// Convert target paths (docs/bg/...) back to source paths (docs/...)
const sourceFiles = brokenFiles.map(f => f.replace(/^docs\/bg\//, 'docs/'));

fs.writeFileSync('scratch/broken_files.txt', sourceFiles.join(' '));
console.log(`Found ${brokenFiles.length} broken files. Saved to scratch/broken_files.txt`);
