const fs = require('fs');
const path = require('path');
const { JSDOM } = require('jsdom');

const ORIGINAL_DIR = path.join(__dirname, '../docs/original');
const REFINED_DIR = path.join(__dirname, '../docs/lektionen');

function getParagraphsFromHtml(html) {
    const dom = new JSDOM(html);
    const elements = dom.window.document.querySelectorAll('p, li, blockquote, h1, h2, h3, h4, h5, h6, td');
    return Array.from(elements)
        .map(el => el.textContent.replace(/\s+/g, ' ').trim())
        .filter(text => text.length > 30);
}

function checkLesson(lessonId) {
    const idStr = lessonId.toString().padStart(2, '0');
    const htmlFile = path.join(ORIGINAL_DIR, `lektion${idStr}.htm`);
    const mdFile = path.join(REFINED_DIR, `lektion${idStr}.md`);

    if (!fs.existsSync(htmlFile) || !fs.existsSync(mdFile)) return;

    const htmlParas = getParagraphsFromHtml(fs.readFileSync(htmlFile, 'utf8'));
    const mdContent = fs.readFileSync(mdFile, 'utf8').replace(/\s+/g, ' ').toLowerCase();

    const missing = htmlParas.filter(para => {
        const normalized = para.toLowerCase();
        return !mdContent.includes(normalized.substring(0, 30));
    });

    // Filter out common metadata
    const filteredMissing = missing.filter(m => {
        return !m.includes('Payer, Alois') && 
               !m.includes('Zitierweise') && 
               !m.includes('http://www.payer.de') &&
               !m.includes('mailto:payer') &&
               !m.includes('Tüpfli\'s Global Village') &&
               !m.includes('Copyright') &&
               !m.includes('Fassung vom') &&
               !m.includes('Zu Lektion') &&
               !m.includes('Schrift mit Diakritika');
    });

    if (filteredMissing.length > 0) {
        console.log(`\n--- Lektion ${idStr}: ${filteredMissing.length} pedagogical blocks missing ---`);
        filteredMissing.slice(0, 10).forEach(m => console.log(`  MISSING: ${m.substring(0, 150)}...`));
    }
}

for (let i = 1; i <= 61; i++) {
    checkLesson(i);
}
