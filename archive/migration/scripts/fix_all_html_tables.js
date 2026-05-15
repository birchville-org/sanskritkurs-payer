const fs = require('fs');
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

const files = [
    'docs/lektionen/lektion57.md',
    'docs/lektionen/uebung04.md',
    'docs/lektionen/uebung06.md',
    'docs/lektionen/uebung07.md',
    'docs/lektionen/uebung09.md',
    'docs/lektionen/uebung14.md',
    'docs/lektionen/uebung19.md',
    'docs/lektionen/uebung34.md',
    'docs/lektionen/uebung39.md',
    'docs/lektionen/uebung59.md',
    'docs/lektionen/uebung60.md'
];

files.forEach(file => {
    if (!fs.existsSync(file)) return;
    let content = fs.readFileSync(file, 'utf8');
    const tableRegex = /<table[\s\S]*?<\/table>/gi;
    content = content.replace(tableRegex, (match) => {
        const dom = new JSDOM(match);
        const table = dom.window.document.querySelector('table');
        return processTable(table);
    });
    
    // Clean up entities and br tags
    content = content.replace(/<br>/gi, '  ');
    content = content.replace(/&nbsp;/gi, ' ');
    content = content.replace(/&lt;/gi, '<');
    content = content.replace(/&gt;/gi, '>');
    content = content.replace(/<span.*?>/gi, '');
    content = content.replace(/<\/span>/gi, '');

    fs.writeFileSync(file, content);
    console.log(`Converted HTML tables in ${file}`);
});
