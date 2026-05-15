import fs from 'fs';
import path from 'path';

const lektionenDir = 'docs/lektionen';

const processFile = (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  
  // 1. Detect 5-column tables that start with empty headers
  // Strategy: Replace the top of these tables with the Gold Standard header
  
  const goldHeader = '| Kasus | Parasmaipada Sg. | Parasmaipada Pl. | Ātmanepada Sg. | Ātmanepada Pl. |';
  const goldSep = '| :--- | :--- | :--- | :--- | :--- |';

  // Regex to find a table starting with empty-ish cells
  // We look for a table that has at least one of the verb categories (Indikativ, Imperfekt, Optativ)
  
  let lines = content.split('\n');
  let newLines = [];
  let inTable = false;
  let currentTable = [];

  const flushTable = () => {
    if (currentTable.length === 0) return;
    
    // Check if this table looks like a Payer verb paradigm
    let text = currentTable.join('\n');
    let isVerbTable = /Indikativ|Imperfekt|Optativ|लट्|लङ्|विधिलिङ्/.test(text);
    
    if (isVerbTable) {
       // Find the first non-separator, non-empty row
       let dataRows = currentTable.filter(r => {
          let c = r.replace(/[| \^:\-]/g, '').trim();
          return c.length > 0 && !r.includes(':---');
       });
       
       if (dataRows.length > 0) {
          // Rebuild the table with the gold header
          let finalRows = [goldHeader, goldSep];
          finalRows.push(...dataRows);
          newLines.push(...finalRows);
          currentTable = [];
          return;
       }
    }
    
    newLines.push(...currentTable);
    currentTable = [];
  };

  for (let line of lines) {
    if (line.trim().startsWith('|')) {
      inTable = true;
      currentTable.push(line);
    } else {
      if (inTable) flushTable();
      newLines.push(line);
      inTable = false;
    }
  }
  flushTable();

  let newContent = newLines.join('\n');
  
  // Final cleanup of redundant markers
  newContent = newContent.replace(/\^\^/g, '&nbsp;'); // Use &nbsp; for visual clarity in code
  newContent = newContent.replace(/[ \t]*&nbsp;[ \t]*/g, ' &nbsp; ');

  if (newContent !== content) {
    fs.writeFileSync(filePath, newContent);
    console.log(`Gold Standard Remediation: ${filePath}`);
  }
};

const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));
files.forEach(file => processFile(path.join(lektionenDir, file)));
