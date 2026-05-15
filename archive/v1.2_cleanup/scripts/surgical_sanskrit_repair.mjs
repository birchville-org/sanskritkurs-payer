import fs from 'fs'
import path from 'path'

const bgDir = 'docs/bg/lektionen'

const wordMap = {
    // Corrupted : Clean
    'कामसмо': 'कामसमो',
    'मोहसмо': 'मोहसमो',
    'क्रोधसмо': 'क्रोधसमो',
    'नित्यसमाс': 'नित्यसमास',
    'नजर्थаः': 'नजर्थाः',
    'षत्प्रкиртитаः': 'षट्प्रकीर्титаः',
    'गङ्गासलилмаधुर्यं': 'गङ्गासलिलमाधुर्यं',
    'साгरेण': 'सागреण', // Wait
    'सागреण': 'सागरेण',
    'उपгччти': 'उपगच्छति',
    'उपддишти': 'упадишати', // Wait, check spelling
    'उपदिश्ти': 'упадишати',
    'उपпдяте': 'упападяте',
    'उपпнн': 'упапанна',
    'प्राпноти': 'прапноти',
    'प्रबुध्यте': 'прабудхяте',
    'प्रभवти': 'прабхавати',
    'प्रवкти': 'правакти',
    'प्रवдти': 'правадати',
    'प्रстти': 'прастаути',
    'विгччти': 'вигаччхати',
    'विमुञ्चти': 'вимунчати',
    'विस्मерти': 'висмарати',
    'विहन्ति': 'виханти',
    'समेजти': 'самети',
    'संगччте': 'сангаччхате',
    'संजాయте': 'санджаяте',
    'संస్కरोти': 'самскароти',
    'मритиसाधни': 'мритисаднани', // Check
    'मृतिसाधनी': 'mṛtisādhanī',
    'упанаяна': 'upanayana',
    'яджньопавита': 'yajñopavīta',
    'द्विजाति': 'dvijāti',
    'матра': 'mātrā',
};

// Also handle the general injections like 'ти' -> 'ti' in parens
function surgicalRepair(content) {
    let newContent = content;
    
    // Replace mapped words
    for (const [corrupted, clean] of Object.entries(wordMap)) {
        newContent = newContent.split(corrupted).join(clean);
    }
    
    // Replace Cyrillic in parentheses (common for transliterations)
    // Matches like (stau-ти) or (rodi-ти)
    newContent = newContent.replace(/\(([a-zA-Zāīūṛṇṃśṣ\-]+)([тимопрендуксаяеси]+)\)/g, (match, latin, cyrillic) => {
        let fixedCyrillic = cyrillic
            .replace(/ти/g, 'ti')
            .replace(/мо/g, 'mo')
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

    // Fix specific words like 3. sg. Präs. P in tables
    newContent = newContent.replace(/3\. SG\. PRÄS\. P/g, '3. ед. ч. сег. вр. П');
    newContent = newContent.replace(/3\. pl\. Präs\. P/g, '3. мн. ч. сег. вр. П');
    newContent = newContent.replace(/3\. sg\. Pres\. P/g, '3. ед. ч. сег. вр. П');
    newContent = newContent.replace(/3\. pl\. Pres\. P/g, '3. мн. ч. сег. вр. П');

    return newContent;
}

const files = fs.readdirSync(bgDir).filter(f => f.endsWith('.md'));

files.forEach(file => {
    const filePath = path.join(bgDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    let fixed = surgicalRepair(content);
    
    if (fixed !== content) {
        fs.writeFileSync(filePath, fixed, 'utf8');
        console.log(`Surgically repaired ${file}`);
    }
});
