#!/usr/bin/env python3
"""Patch the 3 failed replacements in lektion60.md (NBSP issues)."""

path = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion60.md'
with open(path, encoding='utf-8') as f:
    content = f.read()

def replace_exact(content, old, new, label):
    if old not in content:
        print(f'  [!] MATCH FAILED: {label}')
        return content
    result = content.replace(old, new, 1)
    print(f'  [ok] {label}')
    return result

# 1. Remove grammar-box from Beispiele (NBSP in heading)
content = replace_exact(content,
    '#### \xa0Beispiele:\n'
    '\n'
    '::: grammar-box\n'
    '| कृ 8U | चिकीर्षति "er w\xfcnscht zu tun" |\n'
    '| --- | --- |\n'
    '| पत् 1P | पिपतिषति "er ist im Begriffe, zu fallen" |\n'
    '| चुर् 10U | चुचोरयिषति "er w\xfcnscht zu stehlen" |\n'
    '| बुध् Kaus. | बुबोधयिषति "er w\xfcnscht zu belehren (zur Erkenntnis zu wecken)" |\n'
    ':::',

    '#### \xa0Beispiele:\n'
    '\n'
    '| कृ 8U | चिकीर्षति "er w\xfcnscht zu tun" |\n'
    '| --- | --- |\n'
    '| पत् 1P | पिपतिषति "er ist im Begriffe, zu fallen" |\n'
    '| चुर् 10U | चुचोरयिषति "er w\xfcnscht zu stehlen" |\n'
    '| बुध् Kaus. | बुबोधयिषति "er w\xfcnscht zu belehren (zur Erkenntnis zu wecken)" |',
    '60.6 Beispiele grammar-box removed'
)

# 2. Close Zur Reduplikation + open Zu einigen (NBSP before Zu)
content = replace_exact(content,
    '3.  Die besondere Desiderativbildung bestimmter Wurzeln'
    ' siehe bei Kielhorn, Grammatik \xa7 451.\n'
    '\n'
    '\xa0Zu einigen Wurzeln werden Desiderative',

    '3.  Die besondere Desiderativbildung bestimmter Wurzeln'
    ' siehe bei Kielhorn, Grammatik \xa7 451.\n'
    ':::\n'
    '\n'
    '::: grammar-box\n'
    '**Zu einigen Wurzeln werden Desiderative',
    '60.6.1 Zur Reduplikation close + Zu einigen open'
)

# 3. Close Zu einigen box
content = replace_exact(content,
    '**Zu einigen Wurzeln werden Desiderative ohne desiderative Bedeutung gebildet.'
    ' Zu diesen Desiderativen k\xf6nnen Desiderative'
    ' mit desiderativer Bedeutung gebildet werden.\n'
    '\n'
    'Liste bei Kielhorn',

    '**Zu einigen Wurzeln werden Desiderative ohne desiderative Bedeutung gebildet.'
    ' Zu diesen Desiderativen k\xf6nnen Desiderative'
    ' mit desiderativer Bedeutung gebildet werden.**\n'
    ':::\n'
    '\n'
    'Liste bei Kielhorn',
    '60.6.1 Zu einigen Wurzeln close'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('lektion60.md patch done.')
