import fs from 'fs'
import path from 'path'

// Auto-Navigation Generator (Locale-Aware)
export function getSidebarItems(prefix, labelTitle, locale = 'root', groupSize = 0) {
  // Use process.cwd() to ensure reliable path resolution from the project root
  const baseDir = locale === 'en' ? 'docs/en/lektionen' : (locale === 'it' ? 'docs/it/lektionen' : (locale === 'es' ? 'docs/es/lektionen' : 'docs/lektionen'));
  const lektionenDir = path.resolve(process.cwd(), baseDir);
  
  if (!fs.existsSync(lektionenDir)) {
    console.error(`[Sidebar Error] Directory not found: ${lektionenDir}`);
    return [];
  }
  
  const files = fs.readdirSync(lektionenDir).filter(f => f.startsWith(prefix) && f.endsWith('.md'));
  files.sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  
  const linkPrefix = locale === 'root' ? '/lektionen/' : `/${locale}/lektionen/`;
  
  const items = files.map(file => ({
    text: file.replace('.md', '').replace(new RegExp('^' + prefix + '0*', 'i'), labelTitle + ' ').trim(),
    link: linkPrefix + file.replace('.md', '')
  }));

  if (groupSize > 0 && items.length > 0) {
    const groups = [];
    for (let i = 0; i < items.length; i += groupSize) {
      const chunk = items.slice(i, i + groupSize);
      const startText = chunk[0].text.split(' ').pop();
      const endText = chunk[chunk.length - 1].text.split(' ').pop();
      
      groups.push({
        text: `${labelTitle} ${startText} - ${endText}`,
        collapsed: true,
        items: chunk
      });
    }
    return groups;
  }
  return items;
}
