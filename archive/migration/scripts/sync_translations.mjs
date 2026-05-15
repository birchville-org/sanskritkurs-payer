import fs from 'fs';
import path from 'path';

const sourceDirs = ['lektionen', 'schrift', 'uebungen'];
const targetLangs = ['en', 'it', 'es', 'bg', 'uk', 'ru'];
const docsDir = 'docs';

const syncFile = (srcPath, targetLang) => {
  const relPath = path.relative('docs/lektionen', srcPath); // This is a bit brittle, will adjust
};

// Better approach:
sourceDirs.forEach(dir => {
  const srcDir = path.join(docsDir, dir === 'lektionen' ? 'lektionen' : dir);
  if (!fs.existsSync(srcDir)) return;

  const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.md'));

  files.forEach(file => {
    const srcPath = path.join(srcDir, file);
    const srcContent = fs.readFileSync(srcPath, 'utf8');

    targetLangs.forEach(lang => {
      const targetSubDir = path.join(docsDir, lang, dir);
      if (!fs.existsSync(targetSubDir)) fs.mkdirSync(targetSubDir, { recursive: true });

      const targetPath = path.join(targetSubDir, file);
      
      // For now, we OVERWRITE or CREATE with the DE structure
      // We will perform the actual translation in a separate step
      fs.writeFileSync(targetPath, srcContent);
    });
  });
});

console.log('Structural Sync Complete. All languages now have the stabilized DE structure.');
