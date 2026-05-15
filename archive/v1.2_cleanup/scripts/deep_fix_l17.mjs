import fs from 'fs'
import path from 'path'

const locales = ['', 'en', 'bg', 'it', 'es'];

locales.forEach(loc => {
    const dir = loc === '' ? 'docs/lektionen' : `docs/${loc}/lektionen`;
    const filePath = path.join(dir, 'lektion17.md');
    
    if (fs.existsSync(filePath)) {
        let content = fs.readFileSync(filePath, 'utf8');
        
        // Remove the broken table pattern entirely and replace with a clean one
        // Pattern 17.3
        const p173Start = content.indexOf('## 17.3.');
        const p174Start = content.indexOf('## 17.4.');
        
        if (p173Start !== -1 && p174Start !== -1) {
            const section173 = content.substring(p173Start, p174Start);
            
            let newSection173 = section173;
            // Target the broken table area
            // We'll replace everything from > | 3\. sg. to | --- | --- |
            const tableRegex = /> \| (3\..+?Präs\. P|3rd.+?Pres\. P) \| स्तौति \(stau-ti\)[\s\S]+?\| --- \| --- \|/g;
            
            let seeUnder5 = 'siehe unter 5.';
            let or = 'oder';
            let label = '3. sg. Präs. P';
            
            if (loc === 'en') { seeUnder5 = 'see under 5.'; or = 'or'; label = '3rd sg. Pres. P'; }
            if (loc === 'bg') { seeUnder5 = 'вижте под 5.'; or = 'или'; label = '3. sg. Präs. P'; }
            if (loc === 'it') { seeUnder5 = 'vedi sotto 5.'; or = 'o'; label = '3. sg. Präs. P'; }
            if (loc === 'es') { seeUnder5 = 'ver abajo 5.'; or = 'o'; label = '3. sg. Präs. P'; }

            const cleanTable = `> | ${label} | स्तौти (stau-ti) ${or} स्तवीти (${seeUnder5}) |
> | :--- | :--- |`;

            newSection173 = newSection173.replace(tableRegex, cleanTable);
            content = content.replace(section173, newSection173);
        }

        // Fix 17.5 Table - handle the broken Ā entry
        const p175Start = content.indexOf('## 17.5.');
        const p176Start = content.indexOf('## 17.6.');
        
        if (p175Start !== -1 && p176Start !== -1) {
            const section175 = content.substring(p175Start, p176Start);
            let newSection175 = section175;
            
            // Fix the broken Ā row
            // Pattern: > | \n> 3\. pl. Präs. Ā\n>\n> | ब्रुवते (bruv-ate) |
            const brokenRowRegex = /> \|\s*\n>\s*(3\..+?Präs\. Ā|3rd.+?Pres\. Ā)\s*\n>\s*\n>\s*\| ब्रुवते \(bruv-ate\) \|/g;
            newSection175 = newSection175.replace(brokenRowRegex, '> | $1 | ब्रुवते (bruv-ate) |');
            
            // Ensure all tables in this section have align bars
            newSection175 = newSection175.replace(/\| --- \| --- \|/g, '| :--- | :--- |');
            
            content = content.replace(section175, newSection175);
        }

        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Deep fixed L17 tables for ${loc || 'root'}`);
    }
});
