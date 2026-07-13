import os

locales = ['de', 'en', 'it', 'bg', 'ru', 'uk', 'hi', 'fr', 'es', 'ta', 'pa', 'la', 'rm', 'ro', 'id', 'zh-CN', 'he', 'ar', 'arc', 'zh', 'grc', 'fa', 'akk', 'cop', 'th', 'el']

content = """---
layout: doc
title: Settings
---

<ClientOnly>
  <PayerLanguageSettings />
</ClientOnly>
"""

for loc in locales:
    if loc == 'de':
        continue
    dir_path = os.path.join('docs', loc)
    file_path = os.path.join(dir_path, 'settings.md')
    if os.path.exists(dir_path) and not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {file_path}")

