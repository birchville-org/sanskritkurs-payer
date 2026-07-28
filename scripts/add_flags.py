import glob

FLAGS = {
  'de': '🇩🇪', 'en': '🇬🇧', 'it': '🇮🇹', 'ru': '🇷🇺', 'uk': '🇺🇦',
  'hi': '🇮🇳', 'fr': '🇫🇷', 'es': '🇪🇸', 'ta': '🇮🇳', 'pa': '🇮🇳',
  'la': '🏛️', 'rm': '🇨🇭', 'ro': '🇷🇴', 'id': '🇮🇩', 'zh-CN': '🇨🇳',
  'he': '🇮🇱', 'ar': '🇸🇦', 'el': '🇬🇷', 'th': '🇹🇭', 'grc': '🏛️',
  'fi': '🇫🇮', 'hu': '🇭🇺', 'zh': '🇭🇰', 'cop': '🇪🇬', 'fa': '🇮🇷',
  'nl': '🇳🇱', 'am': '🇪🇹', 'af': '🇿🇦', 'lt': '🇱🇹', 'sh': '🇷🇸',
  'sq': '🇦🇱', 'pt': '🇵🇹', 'bg': '🇧🇬', 'arc': '🏛️', 'zh-TW': '🇹🇼'
}

for filepath in glob.glob('/Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/locales/*.mjs'):
    code = filepath.split('/')[-1].replace('.mjs', '')
    flag = FLAGS.get(code, '')
    if not flag:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines[:5]):
        if 'label:' in line and flag not in line:
            # e.g. label: 'DE - Deutsch' -> label: '🇩🇪 DE - Deutsch'
            parts = line.split("'", 2)
            if len(parts) >= 3:
                lines[i] = f"{parts[0]}'{flag} {parts[1]}'{parts[2]}"
            break
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

print("Updated locale flags cleanly.")
