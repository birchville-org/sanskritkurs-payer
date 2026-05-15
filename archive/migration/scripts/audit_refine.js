const fs = require('fs');
const path = require('path');

const LEKTIONEN_DIR = path.join(__dirname, '../docs/lektionen');

function refineFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    const fileName = path.basename(filePath);
    const lessonMatch = fileName.match(/lektion(\d+)\.md/);
    if (!lessonMatch) return;
    
    const lessonId = parseInt(lessonMatch[1], 10);

    // 0. (Removed manual tagging, handled by VitePress plugin)

    // 1. Remove residual artifacts before the first content (handled mostly by master_migrate)
    // Delete EVERYTHING between frontmatter and the first real content (centered block, H1, or box)
    content = content.replace(/(---[\s\S]*?---)[\s\S]*?(?=::: center|::: grammar-box|::: important|# Lektion|## )/i, '$1\n\n');
    
    // 2. Standardize Header Numbering
    // Strip ANY legacy numbering including escaped dots and redundant spaces
    content = content.replace(/^##\s+(\d+\.\d+\.)\s+[\d\.\s\\]*(.*)$/gm, '## $1 $2');
    content = content.replace(/^###\s+(\d+\.\d+\.\d+\.)\s+[\d\.\s\\]*(.*)$/gm, '### $1 $2');

    // 3. De-nest ::: center and Pedagogical Blocks
    // Only if they are directly adjacent
    content = content.replace(/::: center\s*\n\s*::: (grammar-box|important)/g, '::: $1');
    content = content.replace(/::: (grammar-box|important)\s*\n\s*::: center/g, '::: $1');
    
    // 3. De-nest container blocks (avoid > ::: blocks and inner blockquotes in boxes)
    // First, handle the > ::: case
    content = content.replace(/^>\s*:::\s*([\w-]+)\s*?\n([\s\S]*?)\n>\s*:::/gm, (match, type, inner) => {
        const cleanedInner = inner.split('\n').map(line => line.replace(/^>\s?/, '')).join('\n');
        return `::: ${type}\n${cleanedInner}\n:::`;
    });
    
    // Second, handle blockquotes that are entirely inside a box
    content = content.replace(/::: (grammar-box|important)\n+([\s\S]*?)\n+:::/g, (match, type, inner) => {
        if (inner.includes('\n> ') || inner.startsWith('> ')) {
            const cleanedInner = inner.split('\n').map(line => line.replace(/^>\s?/, '')).join('\n');
            return `::: ${type}\n${cleanedInner}\n:::`;
        }
        return match;
    });

    // Cleanup double endings from de-nested blocks
    content = content.replace(/(::: (?:grammar-box|important)[\s\S]*?)\n:::\n:::/g, '$1\n:::');

    // 4. Remove redundant logos and lesson titles at the top
    content = content.replace(/::: center\s*Sanskritkurs\s*:::/gi, '');
    content = content.replace(/::: center\s*\*\*Lektion \d+\*\*\s*:::/gi, '');
    content = content.replace(/::: center\s*# Lektion \d+\s*:::/gi, '');
    content = content.replace(/::: center\s*Lektion \d+\s*:::/gi, '');
    content = content.replace(/::: center\s*#\s*Sanskritkurs\s*:::/gi, '');
    content = content.replace(/::: center\s*\d+\.\s*Lektion \d+\s*:::/gi, '');
    content = content.replace(/::: center\s*!\[\]\(\/images\/sanskritkurslogo\.jpg\)\s*:::/gi, '');
    content = content.replace(/!\[\]\(sanskritkurslogo\.jpg\)/gi, '');
    content = content.replace(/# Sanskritkurs/gi, '');
    
    // 5. Remove redundant logos and mailtos elsewhere
    content = content.replace(/mailto:payer@payer\.de/gi, '');
    content = content.replace(/_Zitierweise \| cite as:_[\s\S]*?URL:.*htm\)/gi, '');

    // 5. Clean up the top area (between H1 and first H2)
    const topAreaRegex = /(# Lektion \d+)([\s\S]*?)(?=##)/i;
    content = content.replace(topAreaRegex, (match, h1, body) => {
        let cleanBody = body.replace(/^([*-]\s*){3,}$/gm, '');
        return h1 + cleanBody;
    });

    // 6. Remove Redundant "Übersicht" Sections
    content = content.replace(/## \d+\.\d+\. (?:Übersicht|uebersicht)[\s\S]*?(?=\n##)/gi, '');

    // 7. Global Spacing Polish
    content = content.replace(/\n{3,}/g, '\n\n'); // Max 2 newlines
    content = content.replace(/^\s+$/gm, ''); // Remove whitespace-only lines
    content = content.replace(/---[\s\n]*---/g, '---'); // Consolidate adjacent HRs elsewhere

    // 8. Final Re-numbering to ensure contiguous sequence (e.g. 2.1, 2.2, 2.3)
    let currentSection = 1;
    content = content.replace(/^##\s+(\d+)\.\d+\.\s+(.*)$/gm, (m, lesson, title) => {
        return `## ${lesson}.${currentSection++}. ${title}`;
    });

    // 9. Clean up double HRs and trailing HRs
    content = content.replace(/\* \* \*\s*\n\s*\* \* \*/g, '* * *');
    content = content.replace(/\* \* \*\s*$/g, '');

    fs.writeFileSync(filePath, content.trim() + '\n', 'utf8');
    console.log(`Polished ${fileName}`);
}

const files = fs.readdirSync(LEKTIONEN_DIR).filter(f => f.startsWith('lektion') && f.endsWith('.md'));
files.forEach(f => {
    if (f !== 'lektion61.md') refineFile(path.join(LEKTIONEN_DIR, f));
});
