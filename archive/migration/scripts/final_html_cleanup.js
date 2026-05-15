const fs = require('fs');
const path = require('path');
const TurndownService = require('turndown');
const { JSDOM } = require('jsdom');

const turndownService = new TurndownService({
    headingStyle: 'atx',
    codeBlockStyle: 'fenced',
    emDelimiter: '_'
});

function processTable(tableNode) {
    const htmlRows = Array.from(tableNode.querySelectorAll('tr'));
    if (htmlRows.length === 0) return '';

    let virtualGrid = [];
    htmlRows.forEach((row, rowIndex) => {
        if (!virtualGrid[rowIndex]) virtualGrid[rowIndex] = [];
        let colIndex = 0;
        Array.from(row.querySelectorAll('td, th')).forEach(cell => {
            while (virtualGrid[rowIndex][colIndex]) colIndex++;
            const rowspan = parseInt(cell.getAttribute('rowspan') || '1', 10);
            const colspan = parseInt(cell.getAttribute('colspan') || '1', 10);
            
            let content = turndownService.turndown(cell.innerHTML).trim().replace(/\n/g, ' <br> ');
            
            for (let r = 0; r < rowspan; r++) {
                for (let c = 0; c < colspan; c++) {
                    if (!virtualGrid[rowIndex + r]) virtualGrid[rowIndex + r] = [];
                    virtualGrid[rowIndex + r][colIndex + c] = {
                        content: (r === 0 && c === 0) ? (content || '&nbsp;') : (r > 0 ? '^^' : '>>'),
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
    for (let r = 0; r < rows; r++) {
        res += '| ' + virtualGrid[r].map(cell => cell.content).join(' | ') + ' |\n';
        if (r === 0) {
            res += '| ' + Array(cols).fill('---').join(' | ') + ' |\n';
        }
    }
    return res + '\n\n';
}

const dir = 'docs/lektionen';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.md'));

files.forEach(fileName => {
    const file = path.join(dir, fileName);
    let content = fs.readFileSync(file, 'utf8');
    let changed = false;

    // Convert HTML tables
    const tableRegex = /<table[\s\S]*?<\/table>/gi;
    if (tableRegex.test(content)) {
        content = content.replace(tableRegex, (match) => {
            const dom = new JSDOM(match);
            const table = dom.window.document.querySelector('table');
            return processTable(table);
        });
        changed = true;
    }

    // General HTML cleanup
    const original = content;
    content = content.replace(/<br>/gi, '  ');
    content = content.replace(/&nbsp;/gi, ' ');
    content = content.replace(/&lt;/gi, '<');
    content = content.replace(/&gt;/gi, '>');
    content = content.replace(/&amp;/gi, '&');
    content = content.replace(/<span.*?>/gi, '');
    content = content.replace(/<\/span>/gi, '');
    content = content.replace(/<ol>/gi, '');
    content = content.replace(/<\/ol>/gi, '');
    content = content.replace(/<li>/gi, '* ');
    content = content.replace(/<\/li>/gi, '');
    content = content.replace(/<nobr>/gi, '');
    content = content.replace(/<\/nobr>/gi, '');
    content = content.replace(/<blockquote>/gi, '> ');
    content = content.replace(/<\/blockquote>/gi, '');
    
    if (content !== original || changed) {
        fs.writeFileSync(file, content);
        console.log(`Cleaned HTML in ${fileName}`);
    }
});
