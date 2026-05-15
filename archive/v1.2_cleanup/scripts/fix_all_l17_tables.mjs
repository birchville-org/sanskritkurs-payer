import fs from 'fs'
import path from 'path'

const locales = ['', 'en', 'bg', 'it', 'es'];

locales.forEach(loc => {
    const dir = loc === '' ? 'docs/lektionen' : `docs/${loc}/lektionen`;
    const filePath = path.join(dir, 'lektion17.md');
    
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Fix 17.3 Table
        // Pattern: > | 3\. sg. Präs. P | स्तौти (stau-ti)\n> oder: स्तवीти siehe unter 5.\n>\n>  |\n> | --- | --- |
        const table173Regex = /> \| (3\..+?Präs\. P) \| स्तौति \(stau-ti\)\s*\n>\s*(?:oder:|or:|или:)\s*स्तवीति.+?\n>\s*\n>\s*\|\s*\n>\s*\| --- \| --- \|/g;
        
        // Language specific "see under 5"
        let seeUnder5 = 'siehe unter 5.';
        if (loc === 'en') seeUnder5 = 'see under 5.';
        if (loc === 'bg') seeUnder5 = 'виж под 5.';
        if (loc === 'it') seeUnder5 = 'vedi sotto 5.';
        if (loc === 'es') seeUnder5 = 'ver abajo 5.';

        content = content.replace(table173Regex, (match, p1) => {
            return `> | ${p1} | स्तौти (stau-ti) ${loc === 'bg' ? 'или' : 'oder'} स्तवीти (${seeUnder5}) |\n> | :--- | :--- |`;
        });

        // Fix 17.5 Table
        // Pattern: > | 3\. sg. Präs. P | ब्रवीти (bravī-ti) |\n> | --- | --- |\n> | 3\. pl. Präs. P | ब्रुвन्ति (bruv-anti) |\n> | 3\. sg. Präs. Ā | ब्रूते (brū-te) |\n> | \n> 3\. pl. Präs. Ā\n>\n>  | ब्रुवते (bruv-ate) |
        const table175Regex = /> \| (3\..+?Präs\. P) \| ब्रवीति \(bravī-ti\) \|\s*\n>\s*\| --- \| --- \|\s*\n>\s*\| (3\..+?Präs\. P) \| ब्रुвन्ति \(bruv-anti\) \|\s*\n>\s*\| (3\..+?Präs\. Ā) \| ब्रूते \(brū-te\) \|\s*\n>\s*\|\s*\n>\s*(3\..+?Präs\. Ā)\s*\n>\s*\n>\s*\| ब्रुवते \(bruv-ate\) \|/g;

        content = content.replace(table175Regex, (match, p1, p2, p3, p4) => {
            return `> | ${p1} | ब्रवीти (bravī-ti) |\n> | :--- | :--- |\n> | ${p2} | ब्रुвन्ति (bruv-anti) |\n> | ${p3} | ब्रूте (brū-te) |\n> | ${p4} | ब्रुवते (bruv-ate) |`;
        });

        // Fallback for slightly different variants (like in English where 166 was different)
        content = content.replace(/> \| 3\. sg\. Pres\. P \| ब्रवीति \(bravī-ti\) \|\n\s+\| --- \| --- \|/g, '> | 3. sg. Pres. P | ब्रवीति (bravī-ti) |\n> | :--- | :--- |');

        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Fixed L17 tables for ${loc || 'root'}`);
    }
});
