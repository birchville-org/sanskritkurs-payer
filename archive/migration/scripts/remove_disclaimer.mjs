import fs from 'fs';
import path from 'path';

const lektionenDir = 'docs/lektionen';

const removeDisclaimer = (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  let lines = content.split('\n');
  
  // Find lines containing the disclaimer
  let newLines = [];
  let skipNextEmpty = false;
  
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes("Tüpfli's Global Village Library") || lines[i].includes("Dieser Text ist Teil der Abteilung Sanskrit")) {
      // Skip this line
      skipNextEmpty = true;
      continue;
    }
    
    if (skipNextEmpty && lines[i].trim() === '') {
      // Skip the empty line immediately following the disclaimer
      continue;
    }
    
    skipNextEmpty = false;
    newLines.push(lines[i]);
  }
  
  let newContent = newLines.join('\n');
  if (newContent !== content) {
    fs.writeFileSync(filePath, newContent);
    console.log(`Removed disclaimer from: ${filePath}`);
  }
};

const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));
files.forEach(file => {
  removeDisclaimer(path.join(lektionenDir, file));
});
