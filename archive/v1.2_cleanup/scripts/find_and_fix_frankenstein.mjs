import fs from 'fs'
import path from 'path'

const bgDir = 'docs/bg/lektionen'

const cyrillicToLatin = {
    'а': 'a', 'е': 'e', 'и': 'i', 'о': 'o', 'у': 'u', 'с': 's', 'р': 'r', 'н': 'n', 'д': 'd', 'к': 'k', 'м': 'm', 'т': 't', 'в': 'v', 'п': 'p', 'я': 'ya'
};

function fixFrankenstein(content) {
    // Regex for Cyrillic characters adjacent to Devanagari
    const frankRegex = /([\u0900-\u097F])([\u0400-\u04FF]+)|([\u0400-\u04FF]+)([\u0900-\u097F])/g;
    
    let newContent = content;
    
    newContent = newContent.replace(frankRegex, (match, d1, c1, c2, d2) => {
        if (d1 && c1) {
            // Devanagari + Cyrillic -> Convert Cyrillic to Latin
            let fixed = Array.from(c1).map(char => cyrillicToLatin[char] || char).join('');
            return d1 + fixed;
        } else if (c2 && d2) {
            // Cyrillic + Devanagari -> Convert Cyrillic to Latin
            let fixed = Array.from(c2).map(char => cyrillicToLatin[char] || char).join('');
            return fixed + d2;
        }
        return match;
    });

    // Also fix the headers that were missed
    newContent = newContent.replace(/3\. sg\. Präs\. P/gi, '3. ед. ч. сег. вр. П');
    newContent = newContent.replace(/3\. pl\. Präs\. P/gi, '3. мн. ч. сег. вр. П');
    newContent = newContent.replace(/3\. sg\. Präs\. Ā/gi, '3. ед. ч. сег. вр. А');
    newContent = newContent.replace(/3\. pl\. Präs\. Ā/gi, '3. мн. ч. сег. вр. А');

    return newContent;
}

const files = fs.readdirSync(bgDir).filter(f => f.endsWith('.md'));

files.forEach(file => {
    const filePath = path.join(bgDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    let fixed = fixFrankenstein(content);
    
    if (fixed !== content) {
        fs.writeFileSync(filePath, fixed, 'utf8');
        console.log(`Frankenstein fixed in ${file}`);
    }
});
