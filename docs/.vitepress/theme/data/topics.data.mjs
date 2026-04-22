import { createContentLoader } from 'vitepress'

const EXCLUSIONS = [
  'lektion', 'übung', 'wortkunde', 'zitierweise', 'rechte', 
  'anmerkung', 'quelle', 'abbildung', 'inhaltsverzeichnis',
  'auf dieser seite', 'impressum', 'bildlizenzen'
];

export default createContentLoader('lektionen/lektion*.md', {
  includeSrc: true,
  transform(raw) {
    const topicMap = {};

    raw.forEach(page => {
      if (!page.url || page.url.includes('/en/')) return;

      const headings = page.src ? (page.src.match(/^#{1,3}\s+(.+)$/gm) || []) : [];
      
      const lessonMatch = page.url.match(/lektion(\d+)/);
      if (!lessonMatch) return;
      
      const lessonNumber = parseInt(lessonMatch[1]);

      headings.forEach(h => {
        if (!h) return;
        let title = h.replace(/^#{1,3}\s+/, '').trim();
        
        // Strip leading numbers/indicators (Latin, Devanagari, letters with closing paren)
        // Handles: "1.1. ", "1. ", "१. ", "A) ", "1) ", "1.1 "
        title = title.replace(/^([\d\.\u0966-\u096F]+|[A-Z]\)|[\d]+\))[\.\s]*/, '').trim();

        const lowerTitle = title.toLowerCase();
        
        if (title.length < 3) return;
        if (EXCLUSIONS.some(ex => lowerTitle.includes(ex))) return;

        if (!topicMap[title]) {
          topicMap[title] = [];
        }
        if (!topicMap[title].includes(lessonNumber)) {
          topicMap[title].push(lessonNumber);
        }
      });
    });

    const sortedTopics = Object.keys(topicMap).sort((a, b) => a.localeCompare(b));
    
    return {
      topics: sortedTopics,
      topicMap: topicMap
    };
  }
})
