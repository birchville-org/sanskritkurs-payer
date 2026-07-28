import os

LOCALES = [
  'de', 'en', 'it', 'ru', 'uk', 'hi', 'fr', 'es', 'ta', 'pa', 
  'la', 'rm', 'ro', 'id', 'zh-CN', 'he', 'ar', 'el', 'th', 'grc',
  'fi', 'hu', 'zh', 'cop', 'fa', 'nl', 'am', 'af', 'lt', 'sh', 'sq', 'pt',
  'bg', 'arc', 'zh-TW', 'akk'
]

BASE_DIR = '/Volumes/SanDisk1TB/proj/Payer/docs'

content = """---
layout: doc
title: Settings
---

<ClientOnly>
  <PayerLanguageSettings />
</ClientOnly>
"""

count = 0
for loc in LOCALES:
    if loc == 'de':
        continue
    loc_dir = os.path.join(BASE_DIR, loc)
    if os.path.exists(loc_dir):
        settings_path = os.path.join(loc_dir, 'settings.md')
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        count += 1

print(f"Created {count} locale settings.md files.")
