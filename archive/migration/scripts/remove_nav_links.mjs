import fs from 'fs';
import path from 'path';

const lektionenDir = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen';
const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));

files.forEach(file => {
  const filePath = path.join(lektionenDir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Remove lines starting with "Zu [Devanāgarī" or "Zu [Lektion" and optional horizontal rule before them
  // We look for a pattern at the end of the file
  
  const lines = content.split('\n');
  let newLines = [...lines];
  let changed = false;

  // Search from the end
  for (let i = lines.length - 1; i >= 0; i--) {
    const line = lines[i].trim();
    if (line.startsWith('Zu [Devanāgarī') || line.startsWith('Zu [Lektion') || line.startsWith('Zu [Schriftübung')) {
      newLines[i] = '';
      changed = true;
      
      // If the previous non-empty line is a divider, remove it too
      let j = i - 1;
      while (j >= 0 && newLines[j].trim() === '') j--;
      if (j >= 0 && (newLines[j].trim() === '* * *' || newLines[j].trim() === '---')) {
        newLines[j] = '';
      }
    }
  }

  if (changed) {
    // Clean up trailing empty lines
    let finalContent = newLines.join('\n').replace(/\n{3,}/g, '\n\n').trim() + '\n';
    fs.writeFileSync(filePath, finalContent);
    console.log(`Cleaned ${file}`);
  }
});
