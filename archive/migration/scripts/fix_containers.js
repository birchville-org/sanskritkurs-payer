const fs = require('fs');
const path = require('path');

const LEKTIONEN_DIR = path.join(__dirname, '../docs/lektionen');

function fixContainers(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // 1. Fix the "empty box followed by text" issue
    // ::: important\n****\n:::\n\n**Text** -> ::: important\n**Text**\n:::
    content = content.replace(/::: (important|grammar-box)\s+\*\*\*\*\s+:::\s*\n\s*\n\s*(.*)/g, '::: $1\n$2\n:::');

    // 2. Remove redundant center around boxes
    content = content.replace(/::: center\s*\n\s*(::: (?:important|grammar-box))/g, '$1');
    content = content.replace(/(::: (?:important|grammar-box)[\s\S]*?:::)\s*\n\s*:::\s*\n/g, '$1\n');

    // 3. Remove stray :::
    content = content.replace(/\n:::\s*\n---/g, '\n---');
    content = content.replace(/---\n:::\n/g, '---\n');

    // 4. Fix specific L10 issue found by subagent
    content = content.replace(/::: important\n\*\*\*\*\n:::\n\n\*\*Sanskrit-Passivsätze/g, '::: important\n**Sanskrit-Passivsätze');

    // 5. (Removed manual tagging flattening, no longer needed)

    fs.writeFileSync(filePath, content, 'utf8');
}

const files = fs.readdirSync(LEKTIONEN_DIR).filter(f => f.startsWith('lektion') && f.endsWith('.md'));
files.forEach(f => fixContainers(path.join(LEKTIONEN_DIR, f)));
console.log('Container fixes applied.');
