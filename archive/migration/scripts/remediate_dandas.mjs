import fs from 'fs';
import path from 'path';

const lektionenDir = 'docs/lektionen';

const fixDandaAccidents = (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  // Pattern 1: Fragmented verse tables (like Lektion 1 or 10)
  // Finds text followed by a single-row table that looks like a verse ending
  const fragmentedVerseRegex = /([^\n]+?)\s*\|\s*&nbsp;\s*\|\s*\n\|\s*:---\s*\|\s*\n/g;
  content = content.replace(fragmentedVerseRegex, '$1\n');

  // Pattern 2: Single line ending in | followed by table separator
  const singleLineDandaTable = /\n([^|\n]+?)\s*\|\s*\n\|\s*:---\s*\|\s*\n/g;
  content = content.replace(singleLineDandaTable, '\n$1\n');

  // Pattern 3: Stray pipes at the end of lines in Sanskrit text (common in exercises)
  // Only if NOT followed by a table structure
  const strayPipeRegex = /([अ-ह।|])\s*\|\s*(\n(?!\s*\|))/g;
  content = content.replace(strayPipeRegex, '$1$2');

  // Pattern 4: Remove accidental table syntax around single sentences
  const singleSentenceTable = /\|\s*([^|\n]+?)\s*\|\s*&nbsp;\s*\|\s*\n\|\s*:---\s*\|\s*\|/g;
  content = content.replace(singleSentenceTable, '$1');

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content);
    console.log(`Repaired Danda accidents in ${path.basename(filePath)}`);
  }
};

const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));
files.forEach(file => fixDandaAccidents(path.join(lektionenDir, file)));
