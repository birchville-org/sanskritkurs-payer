import os, re

bg_dir = "docs/bg/lektionen/"

# Phase 1: Simple string replacements
phase1 = [
    ("Abb.:", "Фигура:"),
    ("\\[Bildquelle:", "\\[Източник на изображението:"),
    ("[Bildquelle:", "[Източник на изображението:"),
    ("Bildquelle:", "Източник на изображението:"),
    ("Zugriff am", "Достъпно на"),
    ("Creative Commons Lizenz (Namensnennung, keine kommerzielle Nutzung, share alike)",
     "Creative Commons лиценз (изисква се признаване, без комерсиална употреба, споделяне при същите условия)"),
    ("Creative Commons Lizenz (Namensnennung)", 
     "Creative Commons лиценз (изисква се признаване)"),
    ("Creative Commons Lizenz",
     "Creative Commons лиценз"),
]

# Phase 2: Known translations
phase2 = [
    ("Übersetzen Sie", "Преведете"),
    ("Beispiele:", "Примери:"),
    ("Beispiel:", "Пример:"),
    ("Bildung:", "Образуване:"),
    ("Maskulinum:", "Мъжки род:"),
    ("Femininum:", "Женски род:"),
    ("Neutrum:", "Среден род:"),
    ("Beachten Sie", "Обърнете внимание"),
    ("Zur Erklärung", "За обяснение"),
    ("Rest wie", "Останалото е като при"),
    ("Bild von", "Снимка от"),
]

# Phase 1+2: Header replacements (line must start with pattern)
header_replacements = [
    ("> [!INFO] Zitierweise & Rechte", "> [!INFO] Цитиране & Права"),
    ("> Dieses Kapitel ist Teil des Sanskritkurses. Details zum Copyright und zur Zitierweise der Ursprungsfassung siehe: [Impressum & Copyright](/impressum)",
     "> Тази глава е част от курса по санскрит. Подробности за авторските права и начина на цитиране на оригиналната версия вижте: [Импресуум & Авторски права](/bg/impressum)"),
]

total_replacements = 0

for f in sorted(os.listdir(bg_dir)):
    if not f.endswith('.md'): continue
    path = bg_dir + f
    with open(path, 'r') as fh:
        content = fh.read()
    
    original = content
    
    # Header replacements (exact line match)
    for old, new in header_replacements:
        content = content.replace(old, new)
    
    # Phase 1
    for old, new in phase1:
        content = content.replace(old, new)
    
    # Phase 2
    for old, new in phase2:
        content = content.replace(old, new)
    
    if content != original:
        changes = sum(1 for a, b in zip(original, content) if a != b)
        with open(path, 'w') as fh:
            fh.write(content)
        # Count actual replacements
        count = 0
        for old, _ in phase1 + phase2 + header_replacements:
            count += original.count(old)
        total_replacements += count
        print(f"Fixed {f}: {count} replacements")

print(f"\nTOTAL: {total_replacements} replacements across all files")
