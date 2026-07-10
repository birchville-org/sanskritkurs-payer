export default {
  async load() {
    const fs = await import('fs')
    const path = await import('path')
    const { fileURLToPath } = await import('url')

    const __filename = fileURLToPath(import.meta.url)
    const __dirname = path.dirname(__filename)

    const EXCLUSIONS = [
      'lektion', 'übung', 'wortkunde', 'zitierweise', 'rechte', 
      'anmerkung', 'quelle', 'abbildung', 'inhaltsverzeichnis',
      'auf dieser seite', 'impressum', 'bildlizenzen'
    ]

    const LOCALES = ['', 'en', 'it', 'es', 'fr', 'hi', 'bg', 'ru', 'uk', 'ta', 'pa', 'la', 'rm', 'ro']

    const baseDir = path.resolve(__dirname, '..', '..')

    function extractTopicsFromDir(localeDir) {
      const topicMap = {}
      if (!fs.existsSync(localeDir)) return topicMap
      
      const files = fs.readdirSync(localeDir).filter(f => /^lektion\d+\.md$/.test(f))
      
      for (const file of files) {
        const lm = file.match(/^lektion(\d+)/)
        if (!lm) continue
        const num = parseInt(lm[1])
        const content = fs.readFileSync(path.join(localeDir, file), 'utf-8')
        const headings = content.match(/^#{2,3}\s+(.+)$/gm) || []
        
        for (const h of headings) {
          let title = h.replace(/^#{2,3}\s+/, '').trim()
          title = title.replace(/^[\d\.\u0966-\u096F]+[.\s]*/, '').trim()
          title = title.replace(/^[A-Z]\)[.\s]*/, '').trim()
          title = title.replace(/^[\d]+\)[.\s]*/, '').trim()
          
          if (title.length < 3) continue
          const lower = title.toLowerCase()
          if (EXCLUSIONS.some(ex => lower.includes(ex))) continue
          
          if (!topicMap[title]) topicMap[title] = []
          if (!topicMap[title].includes(num)) topicMap[title].push(num)
        }
      }
      
      return topicMap
    }

    const localeTopicMap = {}
    for (const locale of LOCALES) {
      const localeDir = path.join(baseDir, locale ? `${locale}/` : '', 'lektionen')
      localeTopicMap[locale] = extractTopicsFromDir(localeDir)
    }

    const deMap = localeTopicMap['']
    const deTopics = Object.keys(deMap).sort((a, b) => a.localeCompare(b))

    return {
      topics: deTopics,
      topicMap: deMap,
      localeTopicMap: localeTopicMap
    }
  }
}
