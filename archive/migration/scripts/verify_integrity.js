const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const ORIGINAL_DIR = path.join(__dirname, '../docs/original');
const REFINED_DIR = path.join(__dirname, '../docs/lektionen');

function getPlaintextFromHtml(html) {
    const dom = new JSDOM(html);
    return dom.window.document.body.textContent.replace(/\s+/g, ' ').trim();
}

function getPlaintextFromMarkdown(md) {
    // Strip YAML frontmatter
    let content = md.replace(/^---[\s\S]*?---/, '');
    // Strip HTML tags
    content = content.replace(/<[^>]*>/g, '');
    // Strip Markdown containers/syntax
    content = content.replace(/::: \w+/g, '');
    content = content.replace(/\[!INFO\]/g, '');
    content = content.replace(/[#*`_\[\]()|:-]/g, ' ');
    return content.replace(/\s+/g, ' ').trim();
}

function verify(lessonId) {
    const idStr = lessonId.toString().padStart(2, '0');
    const htmlFile = path.join(ORIGINAL_DIR, `lektion${idStr}.htm`);
    const mdFile = path.join(REFINED_DIR, `lektion${idStr}.md`);

    if (!fs.existsSync(htmlFile) || !fs.existsSync(mdFile)) {
        console.log(`Skipping Lektion ${idStr} (missing files)`);
        return;
    }

    const htmlText = getPlaintextFromHtml(fs.readFileSync(htmlFile, 'utf8'));
    const mdText = getPlaintextFromMarkdown(fs.readFileSync(mdFile, 'utf8'));

    const htmlWords = htmlText.split(' ').length;
    const mdWords = mdText.split(' ').length;
    const diff = Math.abs(htmlWords - mdWords) / htmlWords;

    console.log(`Lektion ${idStr}: HTML Words: ${htmlWords}, MD Words: ${mdWords}, Diff: ${(diff * 100).toFixed(2)}%`);
    
    if (diff > 0.15) { // 15% threshold for manual check
        console.warn(`[WARNING] Large discrepancy in Lektion ${idStr}! Check for missing content.`);
    }
}

for (let i = 1; i <= 61; i++) {
    verify(i);
}
