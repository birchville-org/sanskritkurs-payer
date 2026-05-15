import fs from 'fs';
import path from 'path';

const lektionenDir = 'docs/lektionen';

const fixDandaAccidentsV2 = (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  // 1. Remove lone separator lines that have no table body or header around them
  // or that follow a line that was clearly not a table header.
  const loneSeparatorRegex = /\n\| :---.*?\n(?!\s*\|)/g;
  content = content.replace(loneSeparatorRegex, '\n');

  // 2. Remove table syntax around single Sanskrit lines
  const singleLineSanskritTable = /\|\s*([^|\n]+?[अ-ह।|][^|\n]*?)\s*\|\s*&nbsp;\s*\|\s*\n\|\s*:---\s*\|\s*\|?\n/g;
  content = content.replace(singleLineSanskritTable, '$1\n');

  // 3. Cleanup remaining orphaned pipes at start/end of lines if not in a table
  const orphanedPipes = /^\s*\|\s*([^|\n]+?[अ-ह।|][^|\n]*?)\s*\|\s*$/gm;
  content = content.replace(orphanedPipes, '$1');

  // 4. Special case: Lektion 10 fragments
  content = content.replace(/\| :--- \| :--- \|\n/g, '');

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content);
    console.log(`Deep-cleaned Danda fragments in ${path.basename(filePath)}`);
  }
};

const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));
files.forEach(file => fixDandaAccidentsV2(path.join(lektionenDir, file)));
