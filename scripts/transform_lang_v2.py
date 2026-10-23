#!/usr/bin/env python3
"""
transform_lang_v2.py — Überträgt das bereinigte v2-Boxensystem von DE auf andere Sprachen.
Entspricht METHODIK_BOXENSYSTEM.md und garantiert 100% Textsegment-Identität.

Validierungs-Gates pro Lektion:
  1. Content Segment Match (100% Text-Erhalt, kein Datenverlust)
  2. Container Balance Check (Opens == Closes)
  3. Structural Container Parity mit docs/lektionen/

Usage:
  python3 scripts/transform_lang_v2.py --lang=en --start=1 --end=3
  python3 scripts/transform_lang_v2.py --lang=fr --start=1 --end=10
  python3 scripts/transform_lang_v2.py --lang=all --start=1 --end=61
"""

import os
import re
import sys
import difflib
import argparse
from pathlib import Path

ROOT = Path(__file__).parent.parent
DE_V2_DIR = ROOT / "docs" / "lektionen"

CITATION_KEYWORDS = [
    'Payer, Alois', 'Quelle:', 'Source:', 'Fonte:', 'Fuente:', 'Источник:',
    'Walker', 'Lüders', 'Dowson', 'Basham', 'Kunnappally', 'Bussmann', 'Kluge', 'Kielhorn',
    '1746', '1876', '1944', '1820', '1869', '1999', '1879', '1959', '1923', 'archive.org'
]

BQ_PREFIX_RE = re.compile(r'^(?:\\?>\s*)+')
DUP_CONTAINER_RE = re.compile(r'^(:::(?:\s+[\w-]+)?)\s*(?:->\s*)?\1$')

def normalize_container_line(s: str) -> str:
    """Normalisiert fehlerhafte Container-Tags (z.B. '::: -> :::', '::: grammar-box ::: grammar-box', '::::')."""
    s = s.strip()
    m = DUP_CONTAINER_RE.match(s)
    if m:
        return m.group(1)
    if s.startswith('::::'):
        s = ':::' + s[4:]
    return s

def extract_content_segments(content_str: str) -> list[str]:
    """Extrahiert alle Textsegmente ohne Frontmatter und Container-Syntax."""
    text = re.sub(r'^---.*?---\s*', '', content_str, flags=re.DOTALL)
    cleaned = []
    for line in text.splitlines():
        s = line.strip()
        if BQ_PREFIX_RE.match(s):
            s = BQ_PREFIX_RE.sub('', s).strip()
        s = normalize_container_line(s)
        if s.startswith('::: note-box ') and not s == '::: note-box':
            title = s[len('::: note-box '):].strip()
            cleaned.append(f'**{title}**')
            continue
        if s.startswith(':::'):
            continue
        s = s.replace('/licenses#', '/images/')
        if s:
            cleaned.append(s)
    return cleaned

def preprocess_body_lines(raw_lines: list[str], lesson_num: int) -> list[str]:
    """Bereinigt strukturelle Übersetzungsartefakte vor der v2-Transformation ohne Textverlust."""
    lines = list(raw_lines)

    # 1. Entferne doppeltes Schliessen durch '::: \<!--  --\>' + Leerzeile + ':::'
    cleaned_1 = []
    i = 0
    n = len(lines)
    while i < n:
        s = lines[i].strip()
        if s.startswith(':::') and ('<!--' in s or '-→' in s):
            cleaned_1.append(':::')
            # Falls nach einer Leerzeile/Textzeile ein überzähliges ':::' vor dem nächsten Container/Header folgt,
            # prüfen wir das im nächsten Schritt oder direkt falls unmittelbar Leerzeile + ':::' folgt:
            if i + 2 < n and lines[i + 1].strip() == '' and lines[i + 2].strip() == ':::':
                i += 3
                continue
            elif i + 4 < n and lines[i + 1].strip() == '' and not lines[i + 2].strip().startswith(':::') and lines[i + 3].strip() == '' and lines[i + 4].strip() == ':::':
                cleaned_1.append(lines[i + 1])
                cleaned_1.append(lines[i + 2])
                i += 5
                continue
            i += 1
            continue
        cleaned_1.append(lines[i])
        i += 1

    # 2. Bereinige duplizierte Container-Zeilen ('::: -> :::', '::: grammar-box ::: grammar-box', '::::')
    # und fehlerhafte '>`-Präfixe auf Containern/Überschriften/Listen in Lektionen ohne echte Blockquotes
    cleaned_2 = []
    in_container = 0
    for idx, line in enumerate(cleaned_1):
        s = line.strip()
        s_norm = normalize_container_line(s)
        if s_norm != s and s_norm.startswith(':::'):
            s = s_norm
            line = s_norm

        if BQ_PREFIX_RE.match(s):
            inner = BQ_PREFIX_RE.sub('', s).strip()
            inner_norm = normalize_container_line(inner)
            # Wenn > vor einem Container-Tag oder Heading steht, oder wir bereits in einem Container sind,
            # oder in einer Lektion, in der im Original kein Blockquote an dieser Stelle existiert:
            is_false_bq = (
                inner_norm.startswith(':::')
                or inner_norm.startswith('#')
                or in_container > 0
                or lesson_num in {35, 37, 41, 52, 61}
                or (lesson_num == 51 and not any(k in inner_norm for k in ['Walker', 'Nowak', 'Johns Hopkins', '1999', '0-8018-5789-9']))
                or (lesson_num == 23 and ('-ra-' in inner_norm or '-ṛ-' in inner_norm))
            )
            if is_false_bq:
                s = inner_norm
                line = inner_norm

        if s.startswith(':::') and len(s) > 3:
            in_container += 1
        elif s == ':::':
            in_container = max(0, in_container - 1)

        cleaned_2.append(line)

    # 3. Balanciere ungeschlossene Container vor dem nächsten Container-Open oder Heading
    # sowie überzählige schliessende ':::' ohne offenes Gegenstück
    cleaned_3 = []
    open_tag = None
    for idx, line in enumerate(cleaned_2):
        s = line.strip()
        if s.startswith(':::') and len(s) > 3:
            if open_tag is not None:
                # Vorheriger Container wurde nicht geschlossen (z.B. lt L51, ru L10, vi L04)
                cleaned_3.append(':::')
            open_tag = s
            cleaned_3.append(line)
        elif s == ':::':
            if open_tag is None:
                # Überzähliges ':::' ohne offenen Container (z.B. sl L10) -> überspringen
                continue
            open_tag = None
            cleaned_3.append(line)
        else:
            cleaned_3.append(line)

    if open_tag is not None:
        cleaned_3.append(':::')

    return cleaned_3

def transform_lesson(orig_text: str, lesson_num: int) -> str:
    """Transformiert eine Lektionsdatei in das v2 Minimal-Set."""
    lines = orig_text.splitlines()
    
    # 1. Frontmatter aktualisieren
    in_fm = False
    fm_lines = []
    raw_body_lines = []
    fm_done = False
    
    for idx, line in enumerate(lines):
        if not fm_done:
            if idx == 0 and line.strip() == '---':
                in_fm = True
                fm_lines.append(line)
                continue
            if in_fm:
                if line.strip() == '---':
                    in_fm = False
                    fm_done = True
                    fm_lines.append(line)
                    continue
                if line.startswith('status:'):
                    fm_lines.append('status: stable')
                elif line.startswith('last_reconstructed:'):
                    fm_lines.append('last_reconstructed: 2026-10-23')
                else:
                    fm_lines.append(line)
                continue
        raw_body_lines.append(line)

    body_lines = preprocess_body_lines(raw_body_lines, lesson_num)
    
    # 2. Body transformieren
    out = []
    i = 0
    n = len(body_lines)
    in_laut_table = False
    grammar_box_count = 0
    
    while i < n:
        line = body_lines[i]
        trimmed = line.strip()
        
        # Replace ::: important -> ::: warning-box
        if trimmed == '::: important':
            out.append('::: warning-box')
            i += 1
            continue
            
        # Replace ::: literatur-box -> ::: note-box (inkl. Konsolidierung)
        if trimmed == '::: literatur-box':
            if len(out) >= 1 and out[-1] == ':::':
                out.pop()
                i += 1
                continue
            if len(out) >= 2 and out[-1] == '' and out[-2] == ':::':
                out.pop()
                out.pop()
                i += 1
                continue
            out.append('::: note-box')
            i += 1
            continue
            
        # Replace ::: center (Verse, Mantras) -> ::: verse-box
        if trimmed == '::: center':
            out.append('::: verse-box')
            i += 1
            continue
            
        # Replace ::: compact -> ::: verse-box
        if trimmed == '::: compact':
            out.append('::: verse-box')
            i += 1
            continue
            
        # Replace ::: metrik-schema -> ::: verse-box
        if trimmed.startswith('::: metrik-schema'):
            out.append('::: verse-box')
            i += 1
            continue
            
        # Strip ::: laut-table (gehört global in CSS)
        if trimmed == '::: laut-table':
            in_laut_table = True
            i += 1
            continue
        if trimmed == ':::' and in_laut_table:
            in_laut_table = False
            i += 1
            continue
            
        # Lektion 1: ::: note-box für Laut-Klassifikation (samānākṣara / समानाक्षर) -> ::: grammar-box
        if lesson_num == 1 and trimmed == '::: note-box':
            lookahead = "\n".join(body_lines[i+1:min(n, i+8)])
            if 'समानाक्षर' in lookahead or 'samānākṣara' in lookahead or 'Klassifikation' in lookahead or 'Classification' in lookahead:
                out.append('::: grammar-box')
                i += 1
                continue

        # Titel aus ::: note-box <Titel> in den Kasteninhalt ziehen
        if trimmed.startswith('::: note-box ') and not trimmed == '::: note-box':
            title = trimmed[len('::: note-box '):].strip()
            out.append('::: note-box')
            out.append(f'**{title}**')
            out.append('')
            i += 1
            continue

        # Schema + Beispiel in der ersten grammar-box von L02, L07, L10 entflechten (Beispiel gehört in ::: indent)
        if trimmed == '::: grammar-box' and i + 1 < n:
            grammar_box_count += 1
            if lesson_num in (2, 7, 10) and grammar_box_count == 1:
                box_lines = []
                j = i + 1
                while j < n and body_lines[j].strip() != ':::':
                    box_lines.append(body_lines[j])
                    j += 1
                
                # Entferne führende/abschliessende Leerzeilen innerhalb der Box
                while box_lines and not box_lines[0].strip():
                    box_lines.pop(0)
                while box_lines and not box_lines[-1].strip():
                    box_lines.pop()
                
                # Suche erste Leerzeile als Trenner zwischen Schema und Beispiel
                blank_idx = None
                for b_idx, bl in enumerate(box_lines):
                    if not bl.strip():
                        blank_idx = b_idx
                        break
                
                if blank_idx is not None:
                    schema_lines = [bl for bl in box_lines[:blank_idx] if bl.strip()]
                    example_lines = [bl for bl in box_lines[blank_idx+1:] if bl.strip()]
                    if schema_lines and example_lines:
                        out.append('::: grammar-box')
                        out.extend(schema_lines)
                        out.append(':::')
                        out.append('')
                        out.append('::: indent')
                        out.extend(example_lines)
                        out.append(':::')
                        i = j + 1
                        continue

        # Blockquotes (>) in ::: note-box (bei Zitaten) oder ::: indent (bei Beispielen) umwandeln
        if BQ_PREFIX_RE.match(trimmed):
            bq_lines = []
            while i < n and (BQ_PREFIX_RE.match(body_lines[i].strip()) or (bq_lines and body_lines[i].strip() == '')):
                if body_lines[i].strip() == '' and (i + 1 < n and not BQ_PREFIX_RE.match(body_lines[i+1].strip())):
                    break
                bq_lines.append(body_lines[i])
                i += 1
            
            raw_bq_text = "\n".join(bq_lines)
            is_citation = any(k in raw_bq_text for k in CITATION_KEYWORDS)
            
            # Vorausschau: Wenn direkt danach literatur-box oder note-box folgt, gehört es zum Zitat
            peek_idx = i
            while peek_idx < n and not body_lines[peek_idx].strip():
                peek_idx += 1
            if peek_idx < n and (body_lines[peek_idx].strip().startswith('::: literatur-box') or body_lines[peek_idx].strip().startswith('::: note-box')):
                is_citation = True
            
            cleaned_bq = []
            for b in bq_lines:
                bs = b.strip()
                if BQ_PREFIX_RE.match(bs):
                    cleaned_bq.append(BQ_PREFIX_RE.sub('', bs).strip())
                else:
                    cleaned_bq.append(b)
                    
            container = 'note-box' if is_citation else 'indent'
            out.append(f'::: {container}')
            for cb in cleaned_bq:
                out.append(cb)
            out.append(':::')
            continue
            
        out.append(line)
        i += 1
        
    return "\n".join(fm_lines) + "\n" + "\n".join(out) + "\n"

def process_language(lang: str, start: int, end: int, out_base: Path = None) -> bool:
    orig_dir = ROOT / "docs" / lang / "lektionen"
    out_dir = (out_base / lang / "lektionen") if out_base else orig_dir
    
    if not orig_dir.exists():
        print(f"❌ Verzeichnis nicht gefunden: {orig_dir}")
        return False
        
    out_dir.mkdir(parents=True, exist_ok=True)
    all_ok = True
    
    print(f"\n{'='*70}")
    print(f"  v2-Struktur-Transformation für Sprache: {lang.upper()} (Lektionen {start:02d}–{end:02d})")
    print(f"{'='*70}")
    
    for num in range(start, end + 1):
        filename = f"lektion{num:02d}.md"
        orig_path = orig_dir / filename
        out_path = out_dir / filename
        de_v2_path = DE_V2_DIR / filename
        
        if not orig_path.exists():
            continue
            
        orig_text = orig_path.read_text(encoding='utf-8')
        v2_text = transform_lesson(orig_text, num)
        out_path.write_text(v2_text, encoding='utf-8')
        
        # 1. Content Segment Audit
        orig_segs = extract_content_segments(orig_text)
        v2_segs = extract_content_segments(v2_text)
        diff = list(difflib.unified_diff(orig_segs, v2_segs, fromfile='orig', tofile='v2', n=0))
        
        if diff:
            print(f"❌ Lektion {num:02d} ({lang}): Textsegment-Mismatch ({len(diff)} Zeilen Diff)!")
            for d in diff[:5]:
                print("   ", d.strip())
            all_ok = False
            continue
            
        # 2. Container Balance Check
        v2_lines = v2_text.splitlines()
        opens = [l.strip() for l in v2_lines if l.strip().startswith(':::') and len(l.strip()) > 3]
        closes = [l.strip() for l in v2_lines if l.strip() == ':::']
        if len(opens) != len(closes):
            print(f"❌ Lektion {num:02d} ({lang}): Container-Disbalance ({len(opens)} Opens vs {len(closes)} Closes)!")
            all_ok = False
            continue
            
        # 3. Structural Parity Check mit DE v2
        parity_str = "Parity N/A (kein DE v2)"
        if de_v2_path.exists():
            de_lines = de_v2_path.read_text(encoding='utf-8').splitlines()
            de_containers = [l.strip().split()[1] if len(l.strip().split()) > 1 else ':::' for l in de_lines if l.strip().startswith(':::')]
            lang_containers = [l.strip().split()[1] if len(l.strip().split()) > 1 else ':::' for l in v2_lines if l.strip().startswith(':::')]
            
            if de_containers == lang_containers:
                parity_str = f"100% Parity ({len(de_containers)} Tags)"
            else:
                parity_str = f"Diff ({len(de_containers)} DE vs {len(lang_containers)} {lang.upper()})"
                
        print(f"✅ Lektion {num:02d} ({lang}): 100% Text-Erhalt ({len(orig_segs)} Segmente) | {len(opens)} Boxen | {parity_str}")
        
    return all_ok

def main():
    parser = argparse.ArgumentParser(description="Payer v2 Struktur-Transfer auf Zielsprachen")
    parser.add_argument("--lang", default="en", help="Sprachcode (z.B. en, fr, it) oder 'all'")
    parser.add_argument("--start", type=int, default=1, help="Start-Lektion (Standard: 1)")
    parser.add_argument("--end", type=int, default=3, help="End-Lektion (Standard: 3)")
    parser.add_argument("--out-base", default=None, help="Optionales Basis-Ausgabeverzeichnis (Standard: docs/)")
    args = parser.parse_args()
    
    if args.lang == "all":
        # Alle Verzeichnisse in docs/ finden, die lektionen/ enthalten
        langs = sorted([d.name for d in (ROOT / "docs").iterdir() if d.is_dir() and (d / "lektionen").exists() and d.name not in ['lektionen', 'v2', 'public', '.vitepress']])
    else:
        langs = [args.lang]
        
    out_base = Path(args.out_base) if args.out_base else None
    success = True
    for l in langs:
        ok = process_language(l, args.start, args.end, out_base=out_base)
        if not ok:
            success = False
            
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
