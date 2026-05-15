import fs from 'fs';
import path from 'path';

const lektionenDir = 'docs/lektionen';

const upgradeToUnicodeDandas = (filePath) => {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  // 1. Replace double pipe || with double danda ॥ if surrounded by Devanagari
  content = content.replace(/([अ-ह।])\s*\|\|\s*/g, '$1 ॥ ');

  // 2. Replace single pipe | with single danda । if at the end of a Devanagari line
  content = content.replace(/([अ-ह।])\s*\|\s*$/gm, '$1 ।');

  // 3. Replace single pipe | with single danda । if between Devanagari words
  content = content.replace(/([अ-ह])\s*\|\s*([अ-ह])/g, '$1 । $2');

  // 4. Special case: Dandas in transliteration lines (if they end with |)
  content = content.replace(/([a-zāīūṛṝḷṅñṭḍṇśṣḥṃ])\s*\|\|\s*$/gm, '$1 ॥');
  content = content.replace(/([a-zāīūṛṝḷṅñṭḍṇśṣḥṃ])\s*\|\s*$/gm, '$1 ।');

  // 5. Cleanup trailing whitespace &nbsp;
  content = content.replace(/[[:space:]]*&nbsp;[[:space:]]*/g, ' ');

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content);
    console.log(`Upgraded to Unicode Dandas in ${path.basename(filePath)}`);
  }
};

const files = fs.readdirSync(lektionenDir).filter(f => f.endsWith('.md'));
files.forEach(file => upgradeToUnicodeDandas(path.join(lektionenDir, file)));
