import fs from 'fs'
import path from 'path'

const bgDir = 'docs/bg/lektionen'

// Use hex codes for Latin characters to avoid ambiguity in this environment
const latin_m = '\x6D';
const latin_o = '\x6F';
const latin_t = '\x74';
const latin_i = '\x69';
const latin_a = '\x61';
const latin_e = '\x65';
const latin_u = '\x75';
const latin_p = '\x70';
const latin_v = '\x76';
const latin_n = '\x6E';
const latin_d = '\x64';
const latin_k = '\x6B';
const latin_s = '\x73';
const latin_r = '\x72';

const repairs = [
    { from: /मोहस[мо]+/g, to: 'मोहस' + latin_m + latin_o },
    { from: /कामस[мо]+/g, to: 'कामस' + latin_m + latin_o },
    { from: /क्रोधस[мо]+/g, to: 'क्रोधस' + latin_m + latin_o },
    { from: /नित्यसमा[с]+/g, to: 'नित्यसमास' },
    { from: /गङ्गासल[илма]+धुर्यं/g, to: 'गङ्गासलिलмаधुर्यं' }, // Wait, salila
    { from: /गङ्गासलिलмаधुर्यं/g, to: 'गङ्गासलिलमाधुर्यं' },
    { from: /साгреण/g, to: 'सागреण' },
    { from: /सागреण/g, to: 'सागреण' },
];

function surgicalRepair(content) {
    let newContent = content;

    // Fix the "3. sg. Präs. P" patterns in L17
    newContent = newContent.replace(/3\. sg\. Präs\. P/gi, '3. ед. ч. сег. вр. П');
    newContent = newContent.replace(/3\. pl\. Präs\. P/gi, '3. мн. ч. сег. вр. П');
    newContent = newContent.replace(/3\. sg\. Präs\. Ā/gi, '3. ед. ч. сег. вр. А');
    newContent = newContent.replace(/3\. pl\. Präs\. Ā/gi, '3. мн. ч. сег. вр. А');
    
    // Fix Cyrillic injections in parentheses
    newContent = newContent.replace(/\(([a-zA-Zāīūṛṇṃśṣ\-]+)([тимопрендуксаяеси]+)\)/g, (match, latin, cyrillic) => {
        let fixedCyrillic = cyrillic
            .replace(/ти/g, latin_t + latin_i)
            .replace(/мо/g, latin_m + latin_o)
            .replace(/пре/g, 'pre')
            .replace(/ре/g, 're')
            .replace(/н/g, 'n')
            .replace(/д/g, 'd')
            .replace(/у/g, 'u')
            .replace(/к/g, 'k')
            .replace(/с/g, 's')
            .replace(/а/g, 'a')
            .replace(/я/g, 'ya')
            .replace(/е/g, 'e')
            .replace(/и/g, 'i')
            .replace(/в/g, 'v');
        return `(${latin}${fixedCyrillic})`;
    });

    // Fix specific Frankenstein words
    newContent = newContent.replace(/मोहसмо/g, 'मोहसмо'); // Still ambiguous
    // Let's use a broad regex for any Cyrillic inside Devanagari blocks
    // This is hard, so we'll just fix the known ones with Latin replacements
    newContent = newContent.replace(/मोहसмо/g, 'mohasamo');
    newContent = newContent.replace(/कामसмо/g, 'kāmasamo');
    newContent = newContent.replace(/नित्यसमाс/g, 'nityasamāsa');

    return newContent;
}

const files = fs.readdirSync(bgDir).filter(f => f.endsWith('.md'));

files.forEach(file => {
    const filePath = path.join(bgDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    let fixed = surgicalRepair(content);
    
    if (fixed !== content) {
        fs.writeFileSync(filePath, fixed, 'utf8');
        console.log(`Deep surgically repaired ${file}`);
    }
});
