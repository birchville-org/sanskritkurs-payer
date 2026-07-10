#!/usr/bin/env python3
import os
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
CONFIG_MJS = ROOT / 'docs/.vitepress/config.mjs'
QA_VIEWER = ROOT / 'docs/public/qa_viewer.html'

def get_locales_from_config():
    content = CONFIG_MJS.read_text(encoding='utf-8')
    match = re.search(r'const allLocales = \[(.*?)\];', content)
    if not match:
        return []
    locales_str = match.group(1).replace(' ', '')
    return [l for l in locales_str.split(',') if l]

LANG_NAMES = {
    'de': 'Deutsch (DE)',
    'en': 'English (EN)',
    'it': 'Italiano (IT)',
    'ru': 'Русский (RU)',
    'uk': 'Українська (UK)',
    'hi': 'हिन्दी (HI)',
    'fr': 'Français (FR)',
    'es': 'Español (ES)',
    'ta': 'தமிழ் (TA)',
    'pa': 'ਪੰਜਾਬੀ (PA)',
    'ro': 'Română (RO)',
    'id': 'Bahasa Indonesia (ID)',
    'he': 'עברית (HE)',
    'zh-CN': 'Simplified Chinese (ZH-CN)',
    'th': 'Thai (TH)',
    'la': 'Latin (LA)',
    'rm': 'Romansh Grischun (RM)',
    'bg': 'Bulgarian (BG)',
    'ar': 'Arabic (AR)',
    'arc': 'Aramaic (ARC)',
    'grc': 'Ancient Greek (GRC)',
    'el': 'Modern Greek (EL)',
    'fa': 'Persian (FA)',
    'akk': 'Akkadian (AKK)',
    'cop': 'Coptic (COP)',
}

def generate_options(locales, default_lang='de'):
    lines = []
    
    # HTML Option
    if default_lang == 'html':
        lines.append('                <option value="qa/lektion01.html" selected>Original HTML</option>')
    else:
        lines.append('                <option value="qa/lektion01.html">Original HTML</option>')

    for l in locales:
        val_lang = 'zh-CN' if l == 'zhCN' else l
        name = LANG_NAMES.get(val_lang, val_lang.upper())
        val = 'lektionen/lektion01' if val_lang == 'de' else f'{val_lang}/lektionen/lektion01'
        selected = ' selected' if l == default_lang else ''
        lines.append(f'                <option value="{val}"{selected}>{name}</option>')
        
    return '\n'.join(lines)

def sync_qa_viewer():
    locales = get_locales_from_config()
    if not locales:
        print("allLocales nicht gefunden.")
        return False
        
    content = QA_VIEWER.read_text(encoding='utf-8')
    
    # Left dropdown (default DE)
    left_opts = generate_options(locales, default_lang='de')
    content = re.sub(
        r'(<select id="left-lang"[^>]*>\n).*?(</select>)',
        r'\g<1>' + left_opts + r'\n            \g<2>',
        content,
        flags=re.DOTALL
    )
    
    # Right dropdown (default HTML)
    right_opts = generate_options(locales, default_lang='html')
    content = re.sub(
        r'(<select id="right-lang"[^>]*>\n).*?(</select>)',
        r'\g<1>' + right_opts + r'\n            \g<2>',
        content,
        flags=re.DOTALL
    )
    
    QA_VIEWER.write_text(content, encoding='utf-8')
    print("QA Viewer Dropdowns synchronisiert.")
    return True

if __name__ == '__main__':
    sync_qa_viewer()
