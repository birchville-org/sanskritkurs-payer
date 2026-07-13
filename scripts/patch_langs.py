import re
from pathlib import Path

ROOT = Path("/Volumes/SanDisk1TB/proj/Payer")

def patch_lan_translate():
    f = ROOT / "scripts/lan_translate.py"
    if not f.exists(): return
    content = f.read_text()
    
    # 1. ACTIVE_LANGS
    if '"am"' not in content:
        content = re.sub(r'("sh", "sq", "akk")', r'\1, "am", "gez"', content)
        
    # 2. LANG_NAMES
    if '"am": "Amharic"' not in content:
        content = re.sub(r'("el": "Modern Greek",)', r'\1 "am": "Amharic", "gez": "Ge\'ez",', content)
        
    # 3. GLOSSARY
    if '"am": {' not in content:
        glossary = """    "am": {
        "title": "የሳንስክሪት ኮርስ",
        "author": "Alois Payer",
        "description": "የሳንስክሪት ሰዋሰው መማሪያ መጽሐፍ",
        "lesson": "ትምህርት",
        "script": "ጽሑፍ",
        "exercise": "መልመጃ"
    },
    "gez": {
        "title": "ትምህርተ ሳንስክሪት",
        "author": "Alois Payer",
        "description": "መጽሐፈ ሰዋስው ዘሳንስክሪት",
        "lesson": "ትምህርት",
        "script": "ጽሑፍ",
        "exercise": "መልመጃ"
    },"""
        content = content.replace('    "el": {', glossary + '\n    "el": {')

    if '"am": {' not in content:
        # Check translation blocks as well
        glossary2 = """    "am": {
        "1. Vorbemerkungen": "1. ቅድመ ሁኔታዎች",
        "1.1. Zur Aussprache": "1.1. ስለ አነባበብ"
    },
    "gez": {
        "1. Vorbemerkungen": "1. ቅድመ ሁኔታዎች",
        "1.1. Zur Aussprache": "1.1. ስለ አነባበብ"
    },"""
        content = content.replace('    "el": {', glossary2 + '\n    "el": {')
        
    f.write_text(content)

def patch_monitor_status():
    f = ROOT / "scripts/monitor_status.py"
    if not f.exists(): return
    content = f.read_text()
    
    if "'am'" not in content:
        content = re.sub(r"('lt', 'sh', 'sq', 'akk')", r"\1, 'am', 'gez'", content)
        
    if '"am":' not in content:
        langs = """    "am": ("አማርኛ", DOCS / "am/lektionen"),
    "gez": ("ግዕዝ", DOCS / "gez/lektionen"),"""
        content = content.replace('    "el": ("Ελληνικά"', langs + '\n    "el": ("Ελληνικά"')
        
    f.write_text(content)

def patch_run_sh():
    f = ROOT / "scripts/run_all_translations.sh"
    if not f.exists(): return
    content = f.read_text()
    if 'am gez' not in content:
        content += "\\npython3 scripts/lan_translate.py --lang am all\\npython3 scripts/lan_translate.py --lang gez all\\n"
        f.write_text(content)

patch_lan_translate()
patch_monitor_status()
patch_run_sh()
print("Done patching.")
