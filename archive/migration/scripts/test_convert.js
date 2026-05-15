const fs = require('fs');
const path = require('path');
const TurndownService = require('turndown');
const { JSDOM } = require('jsdom');

const turndownService = new TurndownService();

const html = fs.readFileSync(path.join(__dirname, '../docs/original/lektion02.htm'), 'utf8');
const dom = new JSDOM(html);
const body = dom.window.document.body;

// Remove boilerplate
const hrElements = body.querySelectorAll('hr');
if (hrElements.length >= 4) {
    // Usually the main content is between the 4th HR and the last HR
    // But let's be more precise
}

const markdown = turndownService.turndown(body.innerHTML);
fs.writeFileSync(path.join(__dirname, 'lektion02_test.md'), markdown);
console.log('Test conversion done.');
