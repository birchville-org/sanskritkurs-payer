import fs from 'fs';
import path from 'path';

const lektionenDir = 'docs/lektionen';

const remediateFile = (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  // 1. Aggressively clean up table rows: remove leading/trailing blockquote markers and legacy colspan symbols
  // This targets the '> | ... | > | --- |' mess.
  content = content.replace(/^[ \t]*>?[ \t]*\|(.*)\|[ \t]*>?[ \t]*$/gm, '|$1|');

  // 2. Fix the "merged separator" lines (often seen in verb tables)
  // Example: '| &nbsp; | परस्मैपदम् || आत्मनेपदम् || | --- | --- | --- | --- | --- |'
  content = content.replace(/^(\|.*)(\|[ \t]*---[ \t]*\|.*)$/gm, (match, p1, p2) => {
    let header = p1.trim();
    if (!header.endsWith('|')) header += ' |';
    let separator = p2.trim();
    if (!separator.endsWith('|')) separator += ' |';
    return `${header}\n${separator}`;
  });

  // 3. Fix the "||" colspan logic: ensure we use ' || ' (2 pipes) for colspans
  // And collapse any '>>' or multiple pipes into the standard ' || '
  let prevContent;
  do {
    prevContent = content;
    // Turn '| >>' or '| ||' into ' || '
    content = content.replace(/\|[ \t]*(?:>>|\|\|)[ \t]*/g, ' || ');
  } while (content !== prevContent);

  // 4. Normalize rowspans: replace '| &nbsp; |' with '| ^^ |'
  content = content.replace(/^\|[ \t]*&nbsp;[ \t]*\|/gm, '| ^^ |');

  // 5. Clean up any remaining legacy ' >' or ' || >' at the end of cells
  content = content.replace(/\|[ \t]*>[ \t]*\|/g, '| |');
  content = content.replace(/\|[ \t]*>[ \t]*$/gm, '|');

  // 6. Final normalization of spaces around markers
  content = content.replace(/[ \t]*\|\|[ \t]*/g, ' || ');
  content = content.replace(/[ \t]*\^\^[ \t]*/g, ' ^^ ');

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content);
    console.log(`Remediated: ${filePath}`);
  }
};

const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));
files.forEach(file => {
  remediateFile(path.join(lektionenDir, file));
});
