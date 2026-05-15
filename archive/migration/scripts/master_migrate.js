const fs = require('fs');
const path = require('path');
const TurndownService = require('turndown');
const { JSDOM } = require('jsdom');

const turndownService = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced',
    emDelimiter: '_'
});

// Disable turndown escaping to preserve ::: syntax
turndownService.escape = (text) => text;

// Multi-Markdown Table Converter (Stable, Clean, Rowspan-enabled)
function processTable(tableNode) {
    const htmlRows = Array.from(tableNode.querySelectorAll('tr'));
    if (htmlRows.length === 0) return '';

    // Pass 1: Build a normalized virtual grid
    let virtualGrid = [];
    htmlRows.forEach((row, rowIndex) => {
        if (!virtualGrid[rowIndex]) virtualGrid[rowIndex] = [];
        let colIndex = 0;
        Array.from(row.querySelectorAll('td, th')).forEach(cell => {
            while (virtualGrid[rowIndex][colIndex]) colIndex++;
            const rowspan = parseInt(cell.getAttribute('rowspan') || '1', 10);
            const colspan = parseInt(cell.getAttribute('colspan') || '1', 10);
            
            // CLEAN TEXT: The VitePress plugin handles Sanskrit coloring automatically!
            let content = turndownService.turndown(cell.innerHTML).trim().replace(/\n/g, ' <br> ');
            
            for (let r = 0; r < rowspan; r++) {
                for (let c = 0; c < colspan; c++) {
                    if (!virtualGrid[rowIndex + r]) virtualGrid[rowIndex + r] = [];
                    virtualGrid[rowIndex + r][colIndex + c] = {
                        content: (r === 0 && c === 0) ? (content || '&nbsp;') : (r > 0 ? '^^' : '>>'),
                        isRowSpan: r > 0,
                        isColSpan: c > 0
                    };
                }
            }
            colIndex += colspan;
        });
    });

    if (virtualGrid.length === 0) return '';
    const rows = virtualGrid.length;
    const cols = virtualGrid[0].length;
    
    let res = '\n\n';
    
    // Step 2: Generate Pipe Table with multimd-table syntax
    // Multi-Markdown tables MUST have a header. If the first row isn't a header, we simulate one.
    for (let r = 0; r < rows; r++) {
        res += '| ' + virtualGrid[r].map(cell => cell.content).join(' | ') + ' |\n';
        if (r === 0) {
            // Separator row
            res += '| ' + Array(cols).fill('---').join(' | ') + ' |\n';
        }
    }
    
    return res + '\n\n';
}

// Rule for ALL tables
turndownService.addRule('universalTable', {
    filter: 'table',
    replacement: function (content, node) {
        const bg = (node.getAttribute('bgcolor') || '').toUpperCase();
        const isPedagogical = (bg === '#FFFFCC' || bg === '#CCFFFF' || bg === '#E2E2E2' || node.innerHTML.includes('lekt1001.jpg'));
        const isImportant = node.innerHTML.includes('lekt1001.jpg') || bg === '#E2E2E2';
        
        const tableContent = processTable(node);
        
        if (isPedagogical) {
            const type = isImportant ? 'important' : 'grammar-box';
            let cleanContent = tableContent.replace(/!\[.*\]\(.*lekt1001\.jpg\)/g, '');
            return `\n\n::: ${type}\n\n${cleanContent.trim()}\n\n:::\n\n`;
        }
        
        return `\n\n${tableContent.trim()}\n\n`;
    }
});

// Rule for centered text
turndownService.addRule('centerText', {
    filter: function (node, options) {
        return (
            (node.getAttribute('align') === 'center' ||
            (node.getAttribute('style') && node.getAttribute('style').includes('text-align: center'))) &&
            node.nodeName !== 'TABLE'
        );
    },
    replacement: function (content) {
        return `\n\n::: center\n\n${content.trim()}\n\n:::\n\n`;
    }
});

const ORIGINAL_DIR = path.join(__dirname, '../docs/original');
const OUTPUT_DIR = path.join(__dirname, '../docs/lektionen');

function migrate(lessonId) {
    const idStr = lessonId.toString().padStart(2, '0');
    const htmlFile = path.join(ORIGINAL_DIR, `lektion${idStr}.htm`);
    if (!fs.existsSync(htmlFile)) return;

    const html = fs.readFileSync(htmlFile, 'utf8');
    const cleanHtml = html.replace(/<!-- SKIP_TRANSLATION_START -->[\s\S]*?<!-- SKIP_TRANSLATION_END -->/gi, '');

    const dom = new JSDOM(cleanHtml);
    const body = dom.window.document.body;

    // Remove nav links
    const navLinksToRemove = [
        /\[Sanskritkurs: Inhaltsverzeichnis\]\(index\.htm\)/gi,
        /\[Sanskritkurs: Wortliste\]\(wortliste\.htm\)/gi,
        /\[Sanskritkurs: Grammatikübersicht\]\(grammatik\.htm\)/gi,
        /\[Lektion \d+\]\(lektion\d+\.htm\)/gi,
        /\[Inhaltsverzeichnis\]\(index\.htm\)/gi,
    ];
    body.querySelectorAll('a').forEach(a => {
        if (navLinksToRemove.some(regex => regex.test(a.outerHTML)) || a.textContent.trim().startsWith('Zu ')) {
            a.remove();
        }
    });

    let markdown = turndownService.turndown(body.innerHTML);

    // 3. Post-processing
    const boilerplatePatterns = [
        /_Erstmals hier publiziert:_.*$/gm,
        /_Überarbeitungen:_.*$/gm,
        /_A__nlass_:.*$/gm,
        /_©opyright_:.*$/gm,
        /Dieser Text ist Teil der Abteilung Sanskrit.*$/gm,
        /Falls Sie die diakritischen Zeichen nicht dargestellt bekommen.*$/gm,
        /Die Devanāgarī-Zeichen sind in Unicode kodiert.*$/gm,
        /Sie benötigen also eine Unicode-Devanāgarī-Schrift\..*$/gm,
        /---[\s\n]*## von Alois Payer[\s\n]*---/gi,
        /## von Alois Payer/gi
    ];
    boilerplatePatterns.forEach(p => { markdown = markdown.replace(p, ''); });

    markdown = markdown.replace(/!\[(.*?)\]\((.*?\.jpg)\)/gi, '![$1](/images/$2)');

    markdown = markdown.replace(/^(#{2,6})\s+(.*)$/gm, (m, hash, title) => {
        return `${hash} ${title.trim()}`;
    });

    let h2Count = 0;
    markdown = markdown.replace(/^(#+) (.*)$/gm, (m, hashes, t) => {
        const originalNumberMatch = t.match(/^(\d+(?:\.\d+)+)\.?\s*/);
        const originalMajorMatch = t.match(/^(\d+)\.?\s*/);
        let cleanTitle = t.replace(/^[\d\.\s\\]+/, '').trim();
        
        if (cleanTitle.toLowerCase() === `lektion ${lessonId}` || cleanTitle.toLowerCase() === 'sanskritkurs') return '';
        if (lessonId === 1 && cleanTitle.toLowerCase() === 'zur aussprache einzelner laute') return `### ${lessonId}.${h2Count}.1. ${cleanTitle}`;
        
        const categoryLabels = ['gesprochenes sanskrit', 'wortschatz', 'vokabeln', 'übung', 'uebung'];
        if (categoryLabels.includes(cleanTitle.toLowerCase())) return `## ${cleanTitle}`;

        if (originalNumberMatch) return `### ${lessonId}.${originalNumberMatch[1]}. ${cleanTitle}`;
        if (originalMajorMatch) {
            h2Count = parseInt(originalMajorMatch[1], 10);
            return `## ${lessonId}.${h2Count}. ${cleanTitle}`;
        }
        return `## ${lessonId}.${++h2Count}. ${cleanTitle}`;
    });

    markdown = markdown.replace(/^#\s*Sanskritkurs\s*/gm, '');
    markdown = markdown.replace(/!\[\]\(sanskritkurslogo\.jpg\)\s*/gi, '');

    markdown = markdown.replace(/^(?<!> )(\*\*[A-Z][^*]+\*\*(?:\*\*)?.*)$/gm, (match) => {
        if (match.includes('--') || match.includes('S. ;') || match.includes('ISBN') || match.includes('Bd.')) return `> ${match}`;
        return match;
    });

    markdown = markdown.replace(/(?<!::: center\s+)(\n!\[\]\(\/images\/.*\)(?:\s*  \n.*)?)/g, (match) => {
        if (match.includes('::: center')) return match;
        return `\n\n::: center\n${match.trim()}\n:::\n\n`;
    });

    const frontmatter = `---
title: "Lektion ${lessonId}"
lesson_id: ${lessonId}
category: "Grammatik"
status: "stable"
last_reconstructed: ${new Date().toISOString().split('T')[0]}
---

# Lektion ${lessonId}

`;

    fs.writeFileSync(path.join(OUTPUT_DIR, `lektion${idStr}.md`), frontmatter + markdown.trim() + '\n');
    console.log(`Master Re-Migrated Lektion ${idStr} (Multi-MD)`);
}

for (let i = 1; i <= 60; i++) {
    migrate(i);
}
