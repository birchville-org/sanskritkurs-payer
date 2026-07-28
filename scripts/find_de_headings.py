import glob, re

GERMAN_HEADING_TERMS = [
    r'\bBildung\b', r'\bEndungen?\b', r'\bPräsensstämme?\b',
    r'\bathematischer?\b', r'\bathematische\b', r'\bPräsensklasse\b', r'\bImperativs?\b',
    r'\bSubjunktivs?\b', r'\bOptativs?\b', r'\bStammes\b', r'\bStämme\b', r'\bFormen\b',
    r'\bZur Form der\b', r'\bBeispiele?\b', r'\bErklärung\b', r'\bGebrauch\b'
]

pattern = re.compile('|'.join(GERMAN_HEADING_TERMS), re.IGNORECASE)

ACTIVE = ['de', 'en', 'it', 'ru', 'uk', 'hi', 'fr', 'es', 'ta', 'pa', 
          'la', 'rm', 'ro', 'id', 'zh-CN', 'he', 'ar', 'el', 'th', 'grc',
          'fi', 'hu', 'zh', 'cop', 'fa', 'nl', 'am', 'pt']

results = {}

for filepath in glob.glob('/Volumes/SanDisk1TB/proj/Payer/docs/*/lektionen/lektion*.md'):
    lang = filepath.split('/')[-3]
    if lang not in ACTIVE or lang == 'de':
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    heading_issues = []
    for idx, line in enumerate(lines, 1):
        if line.startswith('#'):
            clean_heading = re.sub(r'<!--.*?-->', '', line).strip()
            if pattern.search(clean_heading):
                heading_issues.append((idx, clean_heading))
                
    if heading_issues:
        results[filepath] = heading_issues

print(f"Total active language files with German heading terms: {len(results)}")
for path, issues in list(results.items()):
    lang = path.split('/')[-3]
    basename = path.split('/')[-1]
    print(f"\n[{lang}] {basename}: {len(issues)} heading issues")
    for line_num, h in issues[:3]:
        print(f"  L{line_num}: {h}")
