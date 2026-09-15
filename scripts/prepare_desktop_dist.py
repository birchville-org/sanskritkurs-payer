#!/usr/bin/env python3
"""
Extrahiert das DE- und EN-Subset aus docs/.vitepress/dist für die Desktop-App.
Reduziert die Asset-Menge von über 14.000 Dateien (~6,6 GB) auf ca. 850 Dateien (~100 MB).
Bereinigt das Sprachen-Dropdown auf ausschließlich DE und EN und blendet Einstellungen aus.
"""

import os
import sys
import json
import shutil
import re

OTHER_LANGS = [
    'it', 'ru', 'uk', 'hi', 'fr', 'es', 'ta', 'pa', 'la', 'rm', 'ro', 'id', 'zh-CN', 'he', 'ar',
    'el', 'th', 'grc', 'fi', 'hu', 'zh', 'fa', 'bg', 'tr', 'nl', 'af', 'lt', 'sh', 'sq', 'pt',
    'vi', 'am', 'gez', 'pl', 'cs', 'sk', 'sl', 'ka', 'hy', 'si', 'te', 'da', 'no', 'sv', 'is',
    'et', 'zu'
]

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    src_dist = os.path.join(base_dir, 'docs', '.vitepress', 'dist')
    dst_dist = os.path.join(base_dir, 'dist_desktop')

    if not os.path.isdir(src_dist):
        print(f"FEHLER: Quellverzeichnis nicht gefunden: {src_dist}", file=sys.stderr)
        sys.exit(1)

    print(f"Bereinige Zielverzeichnis: {dst_dist}")
    if os.path.exists(dst_dist):
        shutil.rmtree(dst_dist)
    os.makedirs(dst_dist, exist_ok=True)

    # 1. Root-HTML- und Metadateien kopieren
    print("Kopiere Root-Dateien (DE)...")
    for item in os.listdir(src_dist):
        s_item = os.path.join(src_dist, item)
        d_item = os.path.join(dst_dist, item)
        if os.path.isfile(s_item):
            # Vektor-Indizes anderer Sprachen nicht mitkopieren
            if item.startswith('vector_index_') and not (item == 'vector_index.json' or item == 'vector_index_en.json'):
                continue
            shutil.copy2(s_item, d_item)

    # 2. Relevante Verzeichnisse kopieren
    copy_dirs = ['lektionen', 'de', 'en', 'images', 'pwa-icons']
    for cd in copy_dirs:
        s_dir = os.path.join(src_dist, cd)
        d_dir = os.path.join(dst_dist, cd)
        if os.path.isdir(s_dir):
            print(f"Kopiere Ordner: {cd}...")
            shutil.copytree(s_dir, d_dir)

    # 3. Hashmap filtern & relevante Hashes ermitteln
    hashmap_path = os.path.join(src_dist, 'hashmap.json')
    if not os.path.isfile(hashmap_path):
        print(f"WARNUNG: Keine hashmap.json in {src_dist} gefunden.")
        hashes = set()
    else:
        with open(hashmap_path, 'r', encoding='utf-8') as f:
            full_hashmap = json.load(f)

        filtered_hashmap = {}
        for k, v in full_hashmap.items():
            is_other = any(k.startswith(f"{lang}_") for lang in OTHER_LANGS)
            if not is_other:
                filtered_hashmap[k] = v

        with open(os.path.join(dst_dist, 'hashmap.json'), 'w', encoding='utf-8') as f:
            json.dump(filtered_hashmap, f, ensure_ascii=False, indent=2)

        hashes = set(filtered_hashmap.values())
        print(f"Hashmap gefiltert: {len(filtered_hashmap)} / {len(full_hashmap)} Keys beibehalten.")

    # 4. Assets kopieren (nur benötigte Chunks)
    s_assets = os.path.join(src_dist, 'assets')
    d_assets = os.path.join(dst_dist, 'assets')
    os.makedirs(d_assets, exist_ok=True)

    copied_assets = 0
    total_asset_size = 0

    if os.path.isdir(s_assets):
        print("Kopiere gefilterte Assets...")
        for root, dirs, files in os.walk(s_assets):
            rel_path = os.path.relpath(root, s_assets)
            target_sub = os.path.join(d_assets, rel_path) if rel_path != '.' else d_assets
            os.makedirs(target_sub, exist_ok=True)

            for f in files:
                keep = False
                if rel_path == '.' and (f.startswith('app.') or f.endswith('.css') or f.endswith('.woff2') or f.endswith('.woff') or f.endswith('.ttf')):
                    keep = True
                elif rel_path.startswith('chunks'):
                    keep = True
                elif any(h in f for h in hashes):
                    keep = True

                if keep:
                    s_file = os.path.join(root, f)
                    d_file = os.path.join(target_sub, f)
                    shutil.copy2(s_file, d_file)
                    copied_assets += 1
                    total_asset_size += os.path.getsize(s_file)

    print(f"Assets kopiert: {copied_assets} Dateien ({total_asset_size / (1024 * 1024):.2f} MB)")

    # 5. HTML-Dateien bereinigen: Dropdown auf DE/EN beschränken, Einstellungen ausblenden
    print("Bereinige HTML-Dateien (Dropdown nur DE/EN, Einstellungen ausblenden)...")
    
    css_rules = []
    for lang in OTHER_LANGS:
        css_rules.append(f'.VPNavBarTranslations .VPMenuLink:has(a[href^="/{lang}/"])')
        css_rules.append(f'.VPNavBarTranslations .VPMenuLink:has(a[href="/{lang}/"])')
        css_rules.append(f'.VPNavScreenTranslations li:has(a[href^="/{lang}/"])')
        css_rules.append(f'.VPNavScreenTranslations li:has(a[href="/{lang}/"])')
        css_rules.append(f'.VPNavBarTranslations a[href^="/{lang}/"]')
        css_rules.append(f'.VPNavBarTranslations a[href="/{lang}/"]')
        css_rules.append(f'.VPNavScreenTranslations a[href^="/{lang}/"]')
        css_rules.append(f'.VPNavScreenTranslations a[href="/{lang}/"]')

    css_inactive_str = ",\n".join(css_rules) + " {\n  display: none !important;\n}"

    desktop_override_tag = f"""<script id="payer-desktop-init">
window.IS_DESKTOP_APP = true;
try {{
  localStorage.setItem('payer_active_locales', JSON.stringify(['en']));
}} catch (e) {{}}
</script>
<style id="payer-desktop-overrides">
/* 1. Einstellungen (Zahnrad) ausblenden */
.VPNavBar a:has(.nav-gear-icon),
.VPNavScreen a:has(.nav-gear-icon),
.VPNavBar a[href*="settings"],
.VPNavScreen a[href*="settings"],
a:has(.nav-gear-icon),
a[href$="/settings"],
a[href$="/settings.html"],
a[href$="/en/settings"],
a[href$="/en/settings.html"],
.nav-gear-icon {{
  display: none !important;
}}

/* 2. QA Viewer komplett ausblenden */
.VPNavBar a[href*="qa_viewer"],
.VPNavScreen a[href*="qa_viewer"],
a[href*="qa_viewer"],
a[href*="qa_help"] {{
  display: none !important;
}}

/* 3. Sprachen-Dropdown: Alle inaktiven Sprachen ausblenden */
{css_inactive_str}
</style>
"""

    other_langs_pattern = "|".join(re.escape(l) for l in OTHER_LANGS)
    rx_menu_link = re.compile(
        rf'<div class="VPMenuLink"[^>]*><a[^>]*href="/(?:{other_langs_pattern})(?:/|")[^>]*>.*?</a></div>',
        re.DOTALL
    )
    rx_settings_link = re.compile(
        r'<a class="[^"]*VPNavBarMenuLink[^"]*" href="[^"]*settings[^"]*"[^>]*>.*?</a>',
        re.DOTALL
    )
    rx_qa_nav = re.compile(
        r'<a class="[^"]*VPNavBarMenuLink[^"]*" href="[^"]*qa_viewer[^"]*"[^>]*>.*?</a>',
        re.DOTALL
    )
    rx_qa_de_li = re.compile(
        r'<li>\s*<strong>Editoren</strong>:[^<]*<a[^>]*href="[^"]*qa_viewer[^"]*"[^>]*>.*?</li>',
        re.DOTALL
    )
    rx_qa_en_br = re.compile(
        r'<br>\s*<strong>Editors</strong>:[^<]*<a[^>]*href="[^"]*qa_viewer[^"]*"[^>]*>.*?(?=<br>|</div>|</p>)',
        re.DOTALL
    )
    rx_json_qa = re.compile(r',?\{[^{}]*?qa_viewer\.html[^{}]*?\}')

    cleaned_html_count = 0
    for root, dirs, files in os.walk(dst_dist):
        for f in files:
            if f.endswith('.html'):
                file_path = os.path.join(root, f)
                with open(file_path, 'r', encoding='utf-8') as hf:
                    content = hf.read()

                # Statische Links und JSON-Einträge entfernen
                new_content = rx_menu_link.sub('', content)
                new_content = rx_settings_link.sub('', new_content)
                new_content = rx_qa_nav.sub('', new_content)
                new_content = rx_qa_de_li.sub('', new_content)
                new_content = rx_qa_en_br.sub('', new_content)
                new_content = rx_json_qa.sub('', new_content)

                # Overrides einfügen
                if '</head>' in new_content:
                    new_content = new_content.replace('</head>', f'{desktop_override_tag}\n</head>', 1)
                else:
                    new_content = f'{desktop_override_tag}\n' + new_content

                with open(file_path, 'w', encoding='utf-8') as hf:
                    hf.write(new_content)
                cleaned_html_count += 1

    print(f"Bereinigte HTML-Dateien: {cleaned_html_count}")

    # Nicht benötigte Seiten (Settings & QA Viewer) aus Desktop-Dist entfernen
    dead_files = [
        'settings.html', 'settings.md', 'en/settings.html', 'en/settings.md',
        'qa_viewer.html', 'qa_viewer.html.bak', 'qa_help.md'
    ]
    for dead_file in dead_files:
        df_path = os.path.join(dst_dist, dead_file)
        if os.path.exists(df_path):
            os.remove(df_path)

    # 6. Gesamtergebnis berechnen
    total_files = 0
    total_size = 0
    for root, dirs, files in os.walk(dst_dist):
        for f in files:
            fp = os.path.join(root, f)
            total_files += 1
            total_size += os.path.getsize(fp)

    print(f"\nFertig: Desktop-Subset erstellt unter {dst_dist}")
    print(f"Dateien gesamt: {total_files}")
    print(f"Größe gesamt: {total_size / (1024 * 1024):.2f} MB\n")

if __name__ == '__main__':
    main()
