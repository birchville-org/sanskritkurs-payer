import os

SETTINGS_TITLES = {
    'de': 'Einstellungen',
    'en': 'Settings',
    'it': 'Impostazioni',
    'es': 'Configuración',
    'fr': 'Paramètres',
    'ru': 'Настройки',
    'uk': 'Налаштування',
    'rm': 'Parameters',
    'ar': 'الإعدادات',
    'fi': 'Asetukset',
    'ta': 'அமைப்புகள்',
    'pa': 'ਸੈਟਿੰਗਾਂ',
    'la': 'Configurationes',
    'id': 'Pengaturan',
    'th': 'การตั้งค่า',
    'hi': 'सेटिंग्स',
    'el': 'Ρυθμίσεις',
    'grc': 'Ῥυθμίσεις',
    'ro': 'Setări',
    'he': 'הגדרות',
    'hu': 'Beállítások',
    'zh-CN': '设置',
    'am': 'ቅንብሮች',
    'pt': 'Definições',
    'cop': 'Ⲧⲁⲃⲥⲧⲩϥⲓⲛⲅ',
    'af': 'Instellings',
    'nl': 'Instellingen',
    'fa': 'تنظیمات',
    'lt': 'Nustatymai',
    'sh': 'Postavke',
    'sq': 'Cilësimet',
    'zh': '設定',
    'bg': 'Настройки',
    'arc': 'إعدادات',
    'zh-TW': '設定',
    'akk': 'Settings'
}

BASE_DIR = '/Volumes/SanDisk1TB/proj/Payer/docs'

updated = 0
for lang, title in SETTINGS_TITLES.items():
    if lang == 'de':
        path = os.path.join(BASE_DIR, 'settings.md')
    else:
        path = os.path.join(BASE_DIR, lang, 'settings.md')
        
    if os.path.exists(path):
        content = f"""---
layout: doc
title: {title}
---

<ClientOnly>
  <PayerLanguageSettings />
</ClientOnly>
"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1

print(f"Updated Frontmatter titles for {updated} settings.md files.")
