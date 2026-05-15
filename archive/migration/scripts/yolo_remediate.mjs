import fs from 'fs';
import path from 'path';

const lektionenDir = 'docs/lektionen';

const yoloRemediate = (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  // Pass 1: Handle merged lines and leading/trailing junk
  // We split lines that contain a separator mid-way
  let lines = content.split('\n');
  let newLines = [];
  for (let line of lines) {
    // If it looks like a table row
    if (line.trim().includes('|')) {
      // 1. Remove leading/trailing > and spaces
      let cleaned = line.replace(/^[ \t]*>+[ \t]*/, '').replace(/[ \t]*>+[ \t]*$/, '').trim();
      
      // 2. Look for an embedded separator
      if (cleaned.includes('| ---')) {
        // Split at the first occurrence of '| ---'
        let parts = cleaned.split(/(\| ?---)/);
        if (parts.length > 2) {
            let firstPart = parts[0].trim();
            // The separator starts with parts[1] and includes everything after
            let secondPart = (parts[1] + parts.slice(2).join('')).trim();
            
            // Clean up trailing > from first part if any
            firstPart = firstPart.replace(/[ \t]*>[ \t]*$/, '').trim();
            if (!firstPart.endsWith('|')) firstPart += ' |';
            
            newLines.push(firstPart);
            newLines.push(secondPart);
            continue;
        }
      }
      newLines.push(cleaned);
    } else {
      newLines.push(line);
    }
  }
  content = newLines.join('\n');

  // Pass 2: Normalize colspan/rowspan syntax
  // Turn '>>' or '||' or '| ||' into ' || '
  let prevContent;
  do {
    prevContent = content;
    content = content.replace(/\|[ \t]*(?:>>|\|\|)[ \t]*/g, ' || ');
  } while (content !== prevContent);

  // Pass 3: Fix rowspans
  content = content.replace(/^\|[ \t]*&nbsp;[ \t]*\|/gm, '| ^^ |');
  
  // Pass 4: Final cleanup of stray markers
  content = content.replace(/\|[ \t]*>[ \t]*\|/g, '| |');
  content = content.replace(/\|[ \t]*>[ \t]*$/gm, '|');
  content = content.replace(/[ \t]*\|\|[ \t]*/g, ' || ');
  content = content.replace(/[ \t]*\^\^[ \t]*/g, ' ^^ ');

  // Pass 5: Ensure tables have a separator as the first or second line
  // If we find a line with 3+ pipes and no separator nearby, we might need to add one
  // But for now, we just ensure the ones we split are correct.

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content);
    console.log(`YOLO Remediated: ${filePath}`);
  }
};

const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));
files.forEach(file => {
  yoloRemediate(path.join(lektionenDir, file));
});
