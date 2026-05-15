import fs from 'fs';
import path from 'path';

const bgDir = './docs/bg/lektionen';
const keywords = [
    'Wurzel', 'Kasusendung', 'Präsensklasse', 'Übung', 'Wortliste', 'Beispiel',
    'anstatt', 'kann man auch sagen', 'Beachten Sie', 'Weitere Verwendungen',
    'regelmäßigen Endungen', 'Konsonantische Stämme', 'Fragepronomen', 'Vokalische Stämme',
    'Maskulina', 'Neutra', 'Feminina', 'Wortsandhi', 'im Deutschen', 'im Englischen',
    'Bildquelle', 'Abb.:', 'Creative Commons', 'Namensnennung', 'Lizenz',
    'Nominativ', 'Akkusativ', 'Instrumentalis', 'Dativ', 'Ablativ', 'Genetiv', 'Lokativ',
    'Singular', 'Plural', 'Dual', 'Komposita', 'Zusammenfassungsdvandva', 'Kopulative',
    'determinative', 'Possesivkomposita', 'Hinterglied', 'Vorderglied', 'Ablaut',
    'Themavokal', 'Glied', 'Glieder', 'Auflösung', 'einsilbige', 'unregelmäßig',
    'nach', 'oder', 'und', 'insbes.', 'gelegentlich', 'neben', 'statt', 'auslautendem',
    'anlautendem', 'Präsensstämme', 'athematischer', 'thematischer', 'Verbalform',
    'Agens', 'Achtung', 'Fortsetzung', 'Zahlwort', 'Wortwiederholungen', 'Zweisilbige',
    'Wiederholungsübung', 'Gesprochenes', 'Weitere Fragen'
];

const files = fs.readdirSync(bgDir).filter(f => f.endsWith('.md'));
let filesWithIssues = 0;

for (const file of files) {
    const content = fs.readFileSync(path.join(bgDir, file), 'utf8');
    const foundKeywords = keywords.filter(kw => {
        // Simple case-sensitive check for now, but avoids common Bulgarian words if they overlap
        // (e.g. 'и' is Bulgarian for 'and', but also German 'und')
        // We'll look for whole words or specific German strings.
        const regex = new RegExp(`\\b${kw}\\b`, 'i');
        return regex.test(content);
    });

    if (foundKeywords.length > 0) {
        console.log(`[ISSUE] ${file}: Found keywords: ${foundKeywords.join(', ')}`);
        filesWithIssues++;
    }
}

console.log(`\nAudit complete. ${filesWithIssues} files have language mixing issues.`);
if (filesWithIssues > 0) process.exit(1);
