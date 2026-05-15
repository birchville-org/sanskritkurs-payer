import fs from 'fs';
import path from 'path';

function fixLinks(dir, locale) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    if (fs.statSync(filePath).isDirectory()) {
      fixLinks(filePath, locale);
    } else if (file.endsWith('.md')) {
      let content = fs.readFileSync(filePath, 'utf8');
      
      // 1. Replace absolute links
      content = content.replace(/\(\/lektionen\//g, `(/${locale}/lektionen/`);
      content = content.replace(/\(\/uebungen\//g, `(/${locale}/uebungen/`);
      content = content.replace(/\(\/grammatik\)/g, `(/${locale}/grammatik)`);
      content = content.replace(/\(\/impressum\)/g, `(/${locale}/impressum)`);
      content = content.replace(/\(\/themen\)/g, `(/${locale}/themen)`);

      // 2. Escape literal < and > around years (e.g. <1876-1932>)
      content = content.replace(/<(\d{4})/g, '&lt;$1');
      content = content.replace(/(\d{4})>/g, '$1&gt;');
      
      // 3. Close <br> tags
      content = content.replace(/<br>/g, '<br />');
      
      // 4. Fix potential LLM artifact: <|channel>thought blocks
      content = content.replace(/<\|channel>thought[\s\S]*?<channel\|>/g, '');

      fs.writeFileSync(filePath, content);
    }
  });
}

const locale = process.argv[2];
if (!locale) {
  console.error('Usage: node scripts/fix_links_locale.mjs <it|es>');
  process.exit(1);
}

const targetDir = path.join('docs', locale);
if (fs.existsSync(targetDir)) {
  console.log(`Fixing links, escaping HTML, and closing tags for ${locale}...`);
  fixLinks(targetDir, locale);
} else {
  console.error(`Directory not found: ${targetDir}`);
}
