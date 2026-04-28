import fs from 'fs';
import path from 'path';

// Define replacements for Cyrillic characters that frequently creep into Devanagari words
const replacements = [
    // Verbs ending in -ти (Bulgarian) instead of -ति (Sanskrit)
    { from: /([\u0900-\u097F])ти(?!\w)/g, to: '$1ति' },
    
    // Middle of words
    { from: /([\u0900-\u097F])м([\u0900-\u097F])/g, to: '$1म$2' },
    { from: /([\u0900-\u097F])а([\u0900-\u097F])/g, to: '$1ा$2' },
    { from: /([\u0900-\u097F])и([\u0900-\u097F])/g, to: '$1ि$2' },
    { from: /([\u0900-\u097F])т([\u0900-\u097F])/g, to: '$1त$2' },
    { from: /([\u0900-\u097F])с([\u0900-\u097F])/g, to: '$1स$2' },
    
    // Case endings like -ми, -м
    { from: /पञ्चми/g, to: 'पञ्चमी' },
    { from: /सप्तми/g, to: 'सप्तमी' },
    { from: /प्रथма/g, to: 'प्रथमा' },
    { from: /तृतीя/g, to: 'तृतीया' },
    { from: /इмаस्/g, to: 'इमास्' },
    { from: /एताни/g, to: 'एतानि' },
    { from: /नраस्/g, to: 'नरास्' },
    { from: /धेнвस्/g, to: 'धेनवस्' },
    { from: /महान्ти/g, to: 'महान्ति' },
    { from: /अशм्यत/g, to: 'अशम्यत' },
    { from: /м/g, to: (match, offset, string) => {
        // If surrounded by Devanagari, replace with ma
        const prev = string[offset - 1];
        const next = string[offset + 1];
        if (/[\u0900-\u097F]/.test(prev) || /[\u0900-\u097F]/.test(next)) {
            return 'म';
        }
        return match;
    }},
    { from: /т/g, to: (match, offset, string) => {
        const prev = string[offset - 1];
        const next = string[offset + 1];
        if (/[\u0900-\u097F]/.test(prev) || /[\u0900-\u097F]/.test(next)) {
            return 'त';
        }
        return match;
    }},
    { from: /и/g, to: (match, offset, string) => {
        const prev = string[offset - 1];
        const next = string[offset + 1];
        if (/[\u0900-\u097F]/.test(prev)) return 'ि';
        if (/[\u0900-\u097F]/.test(next)) return 'इ';
        return match;
    }},
];

function fixContent(content) {
    let newContent = content;
    
    // Direct string replacements for common ones
    newContent = newContent.replace(/पञ्चми/g, 'पञ्चमी');
    newContent = newContent.replace(/सप्तми/g, 'सप्तमी');
    newContent = newContent.replace(/प्रथма/g, 'प्रथमा');
    newContent = newContent.replace(/द्वितीя/g, 'द्वितीया');
    newContent = newContent.replace(/तृतीя/g, 'तृतीया');
    newContent = newContent.replace(/चतुर्थी/g, 'चतुर्थी'); // Check if this had Cyrillic
    
    // Regex replacements
    replacements.forEach(r => {
        newContent = newContent.replace(r.from, r.to);
    });

    // Final pass for any Cyrillic m/M inside Devanagari strings
    newContent = newContent.replace(/([\u0900-\u097F])[Mм]([\u0900-\u097F])/g, '$1म$2');
    newContent = newContent.replace(/([\u0900-\u097F])[Mм]/g, '$1म');
    newContent = newContent.replace(/[Mм]([\u0900-\u097F])/g, 'म$1');

    return newContent;
}

function processDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            processDir(fullPath);
        } else if (entry.name.endsWith('.md')) {
            const content = fs.readFileSync(fullPath, 'utf-8');
            const fixed = fixContent(content);
            if (content !== fixed) {
                fs.writeFileSync(fullPath, fixed);
                console.log(`Fixed: ${fullPath}`);
            }
        }
    }
}

processDir('docs/bg');
console.log('Bulgarian script cleanup complete.');
