import fs from 'fs';
import path from 'path';

const lektionenDir = 'docs/lektionen';

const removeOverview = (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  // Regex to find ## [Number] Übersicht and everything until the next ## header
  // or until the next major section.
  const overviewRegex = /##\s+(\d+\.\d+\.\s+)?Übersicht\s*?\n([\s\S]*?)(?=\n##\s+)/g;
  
  content = content.replace(overviewRegex, '');

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content.trim() + '\n');
    console.log(`Removed redundant overview from ${path.basename(filePath)}`);
  }
};

const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));
files.forEach(file => removeOverview(path.join(lektionenDir, file)));
