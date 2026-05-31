#!/usr/bin/env python3
"""Apply all signalrot (red-text) fixes across DE lesson files."""
import sys

BASE = "/Volumes/SanDisk1TB/proj/Payer/docs/lektionen"

FIXES = {
    "lektion27.md": [
        ("***रामान्***नास्ति", "***रामान्ना***स्ति"),
    ],
    "lektion33.md": [
        ("3.sg.P.Ind.Präs. **पिपर्ति**", "3.sg.P.Ind.Präs. ***पि***पर्ति"),
        ("3.sg.Ā.Ind.Präs. **मिमीते**", "3.sg.Ā.Ind.Präs. ***मि***मीते"),
        ("3.sg.P.Ind.Präs. **बिभेति**", "3.sg.P.Ind.Präs. ***बि***भेति"),
    ],
    "lektion34.md": [
        ("| भिद् | बिभेद |", "| भिद् | ***बि***भेद |"),
        ("| मुच् | मुमोच |", "| मुच् | ***मु***मोच |"),
        ("| भृ | बभार |", "| भृ | ***ब***भार |"),
    ],
    "lektion42.md": [
        ("durch rot gekennzeichnet", "durch ***rot*** gekennzeichnet"),
        ("***इष्***यति", "***इष***यति"),
        ("स***लक्ष्मणो***", "***सलक्ष्मणो***"),
        ("rot hervorgehobenen", "***rot*** hervorgehobenen"),
    ],
    "lektion44.md": [
        ("(runddhve)", "(run***ddh***ve)"),
        ("(dhugdhve)", "(dhu***gdh***ve)"),
        ("(dviḍḍhve)", "(dvi***ḍḍh***ve)"),
        ('"O Mann!"', '***"O Mann!"***'),
        ("1U आयच्छति", "1***U*** आयच्छति"),
    ],
    "lektion45.md": [
        ("oder युङ्ते", "oder यु***ङ्ते***"),
        ("अरुण्स् (unregelm.!)", "***अरुण्स्*** (unregelm.!)"),
    ],
    "lektion47.md": [
        ('Sie bitte ein', 'Sie ***bitte*** ein'),
    ],
    "lektion48.md": [
        ("3.Kl.: \\-atu", "***3.Kl.: -atu***"),
        ("| शेरताम् |", "| ***शेरताम्*** |"),
        ("स्तुहि[[br]]स्तुवीहि", "स्तुहि[[br]]***स्तुवीहि***"),
        ("स्तुत[[br]]स्तुवीत", "स्तुत[[br]]***स्तुवीत***"),
        ("स्तुष्व[[br]]स्तुवीष्व", "स्तुष्व[[br]]***स्तुवीष्व***"),
        ("स्तुध्वम्[[br]]स्तुवीध्वम्", "स्तुध्वम्[[br]]***स्तुवीध्वम्***"),
        ("स्तौतु[[br]]स्तवीतु", "स्तौतु[[br]]***स्तवीतु***"),
        ("स्तुताम्[[br]]स्तुवीताम्", "स्तुताम्[[br]]***स्तुवीताम्***"),
        ("एधि[[br]](aus:", "***एधि***[[br]](aus:"),
        ("शाधि[[br]](aus:", "***शाधि***[[br]](aus:"),
        ("शासतु[[br]]unregelm.", "***शासतु***[[br]]unregelm."),
        ("जहाहि[[br]]unregelm.", "***जहाहि***[[br]]unregelm."),
        ("लाघवं वैयाकरणस्य", "लाघवं ***वैया***करणस्य"),
        ("द्वयोर्हि कुलयोः शोकम", "***द्वयोर्हि कुलयोः*** शोकम"),
    ],
    "lektion49.md": [
        ("मध्यमः | सुनु | सुनुत", "मध्यमः | ***सुनु*** | सुनुत"),
        ("मध्यमः | तनु | तनुत", "मध्यमः | ***तनु*** | तनुत"),
        ("मध्यमः | कुरु | कुरुत", "मध्यमः | ***कुरु*** | कुरुत"),
        ("मध्यमः | गृहाण | गृह्णीत", "मध्यमः | ***गृहाण*** | गृह्णीत"),
        ("तू्र्ण", "***तू्र्***ण"),
    ],
}

total_applied = 0
total_not_found = 0

for filename, replacements in FIXES.items():
    path = f"{BASE}/{filename}"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    original = content
    for old, new in replacements:
        count = content.count(old)
        if count == 0:
            print(f"  NOT FOUND in {filename}: {repr(old)}")
            total_not_found += 1
        elif count > 1:
            print(f"  AMBIGUOUS ({count}x) in {filename}: {repr(old)}")
        else:
            content = content.replace(old, new, 1)
            print(f"  OK {filename}: {repr(old[:40])} → {repr(new[:40])}")
            total_applied += 1
    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

print(f"\nApplied: {total_applied}, Not found: {total_not_found}")
