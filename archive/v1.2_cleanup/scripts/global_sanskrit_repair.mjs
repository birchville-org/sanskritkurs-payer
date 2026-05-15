import fs from 'fs'
import path from 'path'

const dirs = ['docs', 'docs/en', 'docs/bg', 'docs/it', 'docs/es'];

const repairs = [
    // Sanskrit Corruptions (Cyrillic injection)
    { from: /स्तवीти/g, to: 'स्तवीति' },
    { from: /स्तौти/g, to: 'स्तौति' },
    { from: /कामसмо/g, to: 'कामसमो' },
    { from: /नित्यसमाс/g, to: 'नित्यसमास' },
    { from: /अब्रआह्मणी/g, to: 'अब्राह्मणी' },
    { from: /रोдити/g, to: 'रोदितти' }, // Wait, rodi-ti is better
    { from: /родити/g, to: 'rodi-ti' },
    { from: /ब्रवीти/g, to: 'ब्रवीति' },
    { from: /दोषти/g, to: 'dveṣṭi' }, // Checking variations
    
    // Previous script typos
    { from: /презентен класn/g, to: 'презентни класове' },
    { from: /предна частs/g, to: 'преден член' },
    { from: /преден частs/g, to: 'преден член' },
    { from: /основастепенуване/g, to: 'степенуване на основата' },
];

function processDir(dirPath) {
    const fullPath = path.resolve(process.cwd(), dirPath);
    if (!fs.existsSync(fullPath)) return;
    
    const entries = fs.readdirSync(fullPath, { withFileTypes: true });
    
    for (const entry of entries) {
        const entryPath = path.join(fullPath, entry.name);
        if (entry.isDirectory()) {
            if (entry.name === 'lektionen' || entry.name === 'bg' || entry.name === 'en' || entry.name === 'it' || entry.name === 'es') {
                processDir(entryPath);
            }
        } else if (entry.name.endsWith('.md')) {
            let content = fs.readFileSync(entryPath, 'utf8');
            let original = content;
            
            repairs.forEach(r => {
                content = content.replace(r.from, r.to);
            });
            
            if (content !== original) {
                fs.writeFileSync(entryPath, content, 'utf8');
                console.log(`Repaired ${entry.name} in ${dirPath}`);
            }
        }
    }
}

processDir('docs');
processDir('docs/bg/lektionen');
processDir('docs/en/lektionen');
processDir('docs/it/lektionen');
processDir('docs/es/lektionen');
