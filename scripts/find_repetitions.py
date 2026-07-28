import glob
import re

# Find files with 3 or more repeated words in a row, e.g. "word word word" or "word1 word2 word1 word2 word1 word2"
# Also check for 2-word or 3-word phrase repetitions ( repeated 3+ times)

word_repeat_pattern = re.compile(r'\b(\w{3,})\s+(?:\1\s+){2,}\1\b', re.IGNORECASE)
phrase_repeat_pattern = re.compile(r'(\b\w+\s+\w+\b)(?:\s+\1){2,}', re.IGNORECASE)

findings = []

for filepath in glob.glob('/Volumes/SanDisk1TB/proj/Payer/docs/*/lektionen/lektion*.md'):
    lang = filepath.split('/')[-3]
    filename = filepath.split('/')[-1]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Search for single word repetitions
    for match in word_repeat_pattern.finditer(content):
        # get line number
        line_no = content[:match.start()].count('\n') + 1
        word = match.group(1)
        count = len(re.findall(rf'\b{re.escape(word)}\b', match.group(0), re.IGNORECASE))
        findings.append({
            'lang': lang,
            'file': filename,
            'line': line_no,
            'snippet': match.group(0)[:60] + '...',
            'repeat_count': count,
            'type': 'word'
        })

    # Search for 2-word phrase repetitions
    for match in phrase_repeat_pattern.finditer(content):
        line_no = content[:match.start()].count('\n') + 1
        phrase = match.group(1)
        findings.append({
            'lang': lang,
            'file': filename,
            'line': line_no,
            'snippet': match.group(0)[:60] + '...',
            'repeat_count': 3,
            'type': 'phrase'
        })

print(f"Total repetitive anomalies found: {len(findings)}")
print("-" * 80)
# Sort by language and file
findings.sort(key=lambda x: (x['lang'], x['file'], x['line']))
for f in findings:
    print(f"[{f['lang']}] {f['file']} (L{f['line']}): {f['type']} -> {f['snippet']}")
