import fs from 'fs';
import path from 'path';

const globalFiles = ['index.md', 'grammatik.md', 'impressum.md', 'licenses.md', 'themen.md'];
const targetLangs = ['en', 'it', 'es', 'bg', 'uk', 'ru'];
const docsDir = 'docs';

globalFiles.forEach(file => {
  const srcPath = path.join(docsDir, file);
  if (!fs.existsSync(srcPath)) return;
  const srcContent = fs.readFileSync(srcPath, 'utf8');

  targetLangs.forEach(lang => {
    const targetPath = path.join(docsDir, lang, file);
    // Note: These should ideally be translated too, but structural sync is step 1
    fs.writeFileSync(targetPath, srcContent);
  });
});

console.log('Global Files Synced.');
