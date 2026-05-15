import re

filepath = '/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/lektion04.md'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # Find < not followed by a known tag
    matches = re.finditer(r'<(?!/?(?:table|tbody|tr|td|br|b|i|strong|em|p|div|span|script|img|a|h[1-6]|ul|ol|li|thead|tfoot|th|blockquote|hr|sub|sup|cite|!--))', line)
    for match in matches:
        print(f"Line {i+1}, Column {match.start()+1}: {line[match.start():match.start()+10]}")
