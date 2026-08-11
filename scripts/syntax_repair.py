#!/usr/bin/env python3
"""
scripts/syntax_repair.py — Vollständige Syntax-Check & Repair-Routine
für DE-Lektionen (docs/lektionen/*.md)

Prüft und repariert:
  A) Container-Tiefe: schließende ::: müssen dieselbe Anzahl Doppelpunkte
     haben wie ihr öffnender Tag. Korrekte Tiefe wird stack-basiert ermittelt.
  B) Unclosed containers werden direkt nach dem letzten inneren Container
     geschlossen, nicht erst am Dateiende.

Signalrot-Fehler werden nur gemeldet (kein Auto-Fix, da zu risikoreich).

Usage:
  python3 scripts/syntax_repair.py              # check only (kein Fix)
  python3 scripts/syntax_repair.py --fix        # repariert Container-Fehler
  python3 scripts/syntax_repair.py --fix --file docs/lektionen/lektion04.md
  python3 scripts/syntax_repair.py --fix --lektionen   # nur lektion*.md
  python3 scripts/syntax_repair.py --fix --uebungen    # nur uebung*.md
  python3 scripts/syntax_repair.py --fix --all         # alles (default)
"""

import re, sys, html as html_mod
from pathlib import Path

ROOT   = Path(__file__).parent.parent
QA_DIR = ROOT / "docs/public/qa"
DOCS   = ROOT / "docs"
LEKT   = ROOT / "docs/lektionen"

# ── Dateiauswahl ──────────────────────────────────────────────────────────────

def collect_files(mode: str, single: str = None) -> list:
    if single:
        p = Path(single)
        if not p.is_absolute():
            p = ROOT / p
        return [p] if p.exists() else []
    
    files = []
    if mode == 'all':
        for f in DOCS.rglob("*.md"):
            if ".vitepress" not in f.parts and "node_modules" not in f.parts:
                files.append(f)
    else:
        for f in LEKT.iterdir():
            if f.suffix != '.md':
                continue
            n = f.name
            if mode == 'lektionen' and re.match(r'^lektion\d+\.md$', n):
                files.append(f)
            if mode == 'uebungen' and re.match(r'^uebung\d+\.md$', n):
                files.append(f)
    
    # Sort files for deterministic output
    return sorted(files)


# ── Container-Analyse & Repair ────────────────────────────────────────────────

# Öffner: Colons gefolgt von einem alphabetischen Tag (grammar-box, media, ...)
OPEN_RE  = re.compile(r'^(:{3,})\s*([A-Za-z]\S*)(.*)')
# Schließer: nur Colons, optional trailing whitespace
CLOSE_RE = re.compile(r'^(:{3,})\s*$')
# Einzel-Tag auf eigener Zeile (falsch getrennter Öffner: :::↵tag-name)
VALID_TAGS = ['center', 'media', 'note-box', 'grammar-box', 'important', 'tip', 'warning', 'info', 'danger', 'details', 'laut-table', 'metrik-schema', 'indent', 'no-header']
LONE_TAG_RE = re.compile(rf'^({"|".join(VALID_TAGS)})(?:\s+.*)?$')


def fix_split_tags(lines: list, changes: list) -> list:
    """
    Erkennt das Muster:
        :::           ← echter Schließer ODER fehlerhafter Öffner-Anfang
        tag-name      ← einzelner Bezeichner auf eigener Zeile
        ...content...
        :::           ← Schließer des (split) Containers

    Wenn ':::' + 'tag-name' ein ÖFFNER ist (d.h. es gibt einen passenden
    Schließer danach), werden die zwei Zeilen zu ':::tag-name' zusammengeführt
    und der überflüssige Schließer am Ende entfernt.

    Heuristik: wenn 'tag-name' nach einem Schließer (Stack leer) kommt,
    ist es ein split Öffner. Wenn es nach einem Öffner kommt, ist es Freitext.
    """
    result = []
    i = 0
    # Quick pass: merge split openers
    while i < len(lines):
        line = lines[i]
        mc = CLOSE_RE.match(line)
        # Prüfe ob nächste Zeile ein lone tag ist
        if mc and i + 1 < len(lines):
            next_line = lines[i + 1]
            tm = LONE_TAG_RE.match(next_line)
            if tm:
                merged = mc.group(1) + next_line.strip()
                changes.append(
                    f"  L{i+1}: MERGE {line!r} + {next_line!r} → {merged!r}"
                )
                result.append(merged)
                i += 2
                continue
        result.append(line)
        i += 1
    return result




def repair_containers(path: Path, fix: bool = False) -> list:
    """
    Stack-basierter Container-Fixer mit korrekter Schließer-Einschub-Logik.

    Wenn ein zu-tiefer Schließer einen inneren Container schließt und dabei
    noch äußere Container offenlässt, werden die äußeren Schließer SOFORT
    nach dem inneren Schließer eingefügt (nicht ans Dateiende).

    Rückgabe: Liste von change-Strings. Leer = keine Änderung.
    """
    content = path.read_text(encoding='utf-8')
    lines   = content.split('\n')
    result  = []   # Ausgabe-Zeilen
    stack   = []   # (depth, tag, result_idx)  — LIFO
    changes = []

    # Pre-Processing: merge falsch getrennter Öffner (:::↵tag-name)
    lines = fix_split_tags(lines, changes)

    # Puffer für Schließer die direkt VOR der nächsten Zeile eingefügt werden
    pending = []   # list of (close_str, change_str)

    def flush():
        for cs, ch in pending:
            result.append(cs)
            changes.append(ch)
        pending.clear()

    for lineno, line in enumerate(lines, 1):
        if line.strip().startswith('#'):
            flush()
            while stack:
                top_d, top_tag, top_ri = stack.pop()
                correct = ':' * top_d
                changes.append(
                    f"  L{lineno}: INSERT {correct!r} (Auto-close {top_tag} before heading)"
                )
                result.append(correct)

        mo = OPEN_RE.match(line)
        mc = CLOSE_RE.match(line)

        if mo:
            flush()
            d   = len(mo.group(1))
            tag = mo.group(2)
            
            original_d = d
            # Enforce strict nesting limits:
            # - If not stack OR tag is strictly top-level, it must be exactly 3 colons.
            # - Else if stack is not empty, max nesting depth is 3 (max 5 colons).
            if not stack or tag in ('grammar-box', 'deleteme-box'):
                if d != 3:
                    d = 3
                    line = ':' * d + ' ' + tag + mo.group(3)
                    changes.append(f"  L{lineno}: NORMALIZE OPENER {':'*original_d + ' ' + tag} -> {':'*d + ' ' + tag}")
            else:
                # Nested opener: must be at most 5 colons
                if d >= 6:
                    d = min(5, stack[-1][0] + 1)
                    line = ':' * d + ' ' + tag + mo.group(3)
                    changes.append(f"  L{lineno}: NORMALIZE OPENER {':'*original_d + ' ' + tag} -> {':'*d + ' ' + tag}")
            
            # Wenn ein neuer Öffner kommt, der nicht tiefer als der aktuelle Stack ist,
            # müssen wir die noch offenen (zu tiefen) Container zuerst schließen!
            # Denn in VitePress muss ein nested Container IMMER mehr Colons haben.
            while stack and d <= stack[-1][0]:
                top_d, top_tag, top_ri = stack.pop()
                correct = ':' * top_d
                changes.append(
                    f"  L{lineno}: INSERT {correct!r} (Auto-close {top_tag} vor neuem {tag})"
                )
                result.append(correct)

            result.append(line)
            stack.append((d, tag, len(result) - 1))

        elif mc:
            actual = len(mc.group(1))

            if not stack:
                flush()
                # Orphan Schließer (Stack leer) -> LÖSCHEN (nicht in result aufnehmen!)
                changes.append(f"  L{lineno}: DELETE ORPHAN {mc.group(1)!r}")
                continue

            else:
                top_d, top_tag, top_ri = stack[-1]

                if actual == top_d:
                    # Perfekte Übereinstimmung
                    flush()
                    result.append(line)
                    stack.pop()

                elif actual > top_d:
                    # Schließer zu tief: korrigiere auf Stack-Top-Tiefe
                    flush()
                    correct = ':' * top_d
                    changes.append(
                        f"  L{lineno}: {mc.group(1)!r} → {correct!r}"
                        f"  ({':'*top_d}{top_tag} @ L{top_ri+1})"
                    )
                    result.append(correct)
                    stack.pop()

                    # Äußere Container die durch diesen (zu tiefen) Schließer
                    # ebenfalls gemeint waren, sofort pending:
                    # Heuristik: wenn der ursprüngliche actual >= parent_depth
                    # (d.h. der Schließer war tief genug, um auch parent zu
                    # schließen), schließe parent direkt danach.
                    while stack:
                        pd, ptag, pri = stack[-1]
                        if actual >= pd:
                            pc = ':' * pd
                            pending.append((
                                pc,
                                f"  L{lineno}: AUTO {pc!r}"
                                f"  ({':'*pd}{ptag} @ L{pri+1})"
                            ))
                            stack.pop()
                        else:
                            break

                else:
                    # Schließer zu flach: schließe tiefere Container zuerst
                    flush()
                    while stack and stack[-1][0] > actual:
                        id_, itag, iri = stack.pop()
                        ic = ':' * id_
                        result.append(ic)
                        changes.append(
                            f"  L{lineno}: INSERT {ic!r}"
                            f"  ({':'*id_}{itag} @ L{iri+1})"
                        )
                    if stack and stack[-1][0] == actual:
                        result.append(line)
                        stack.pop()
                    elif stack:
                        correct = ':' * stack[-1][0]
                        changes.append(
                            f"  L{lineno}: {mc.group(1)!r} → {correct!r}"
                            f"  ({stack[-1][1]})"
                        )
                        result.append(correct)
                        stack.pop()
                    else:
                        result.append(line)
        else:
            flush()
            result.append(line)

    # Pending nach letzter Zeile
    flush()

    # Noch offene Container am Dateiende schließen
    while stack:
        d, tag, ri = stack.pop()
        ac = ':' * d
        result.append(ac)
        changes.append(f"  EOF: {ac!r}  ({':'*d}{tag} @ L{ri+1})")

    if changes and fix:
        path.write_text('\n'.join(result), encoding='utf-8')

    return changes


# ── Signalrot-Check ───────────────────────────────────────────────────────────

def _red_texts(html_path: Path) -> list:
    src = html_mod.unescape(
        html_path.read_text(encoding='utf-8', errors='replace')
    )
    raw_list = re.findall(
        r'<font[^>]*color="#?FF0000[^>]*>([\s\S]*?)</font>', src, re.I
    )
    out = []
    for raw in raw_list:
        t = re.sub(r'<[^>]+>', '', raw).strip()
        t = re.sub(r'\s+', ' ', t)
        if t:
            out.append(t)
    return out


def check_signalrot(path: Path) -> list:
    m = re.search(r'lektion(\d+)\.md$', str(path))
    if not m:
        return []
    html_path = QA_DIR / f"lektion{m.group(1)}.html"
    if not html_path.exists():
        return []

    content   = path.read_text(encoding='utf-8', errors='replace')
    red_texts = _red_texts(html_path)
    if not red_texts:
        return []

    METRIK = {'˘': '◡', 'ˉ': '—'}
    missing = []
    for text in red_texts:
        esc   = re.sub(r'^-', r'\\-', text)
        equiv = ' '.join(METRIK.get(c, c) for c in text)
        pats  = [
            r'\*+' + re.escape(text)  + r'\*+',
            r'\*+' + re.escape(esc)   + r'\*+',
            r'\*+' + re.escape(equiv) + r'\*+',
            r'^#{1,6}\s+.*' + re.escape(text),
        ]
        if not any(re.search(p, content, re.MULTILINE) for p in pats):
            missing.append(text)

    if missing:
        total = len(red_texts)
        found = total - len(missing)
        sample = ', '.join(repr(t) for t in missing[:6])
        extra  = f" … (+{len(missing)-6} mehr)" if len(missing) > 6 else ""
        return [f"  ⚠ Signalrot {found}/{total} fehlt: {sample}{extra}"]
    return []


# ── Hauptprogramm ─────────────────────────────────────────────────────────────

def main():
    args   = sys.argv[1:]
    fix    = '--fix'       in args
    mode   = 'all'
    single = None

    i = 0
    while i < len(args):
        a = args[i]
        if   a == '--lektionen': mode = 'lektionen'
        elif a == '--uebungen':  mode = 'uebungen'
        elif a == '--all':       mode = 'all'
        elif a.startswith('--file='):
            single = a[7:]
        elif a == '--file' and i + 1 < len(args):
            single = args[i + 1]; i += 1
        i += 1

    files = collect_files(mode, single)
    if not files:
        print("Keine Dateien gefunden."); sys.exit(1)

    tag = '& REPAIR' if fix else '(nur Prüfung)'
    print(f"\n{'='*65}")
    print(f"  Syntax-Check {tag}  —  {len(files)} Dateien")
    print(f"{'='*65}\n")

    total_ct = 0   # container issues
    total_sr = 0   # signalrot issues
    n_err    = 0

    for path in files:
        ct = repair_containers(path, fix=fix)
        sr = check_signalrot(path)

        if ct or sr:
            rel = path.relative_to(ROOT)
            icon = '✓' if (fix and ct) else '❌'
            print(f"{icon} {rel}:")
            if ct:
                verb = 'repariert' if fix else 'gefunden'
                print(f"  Container ({len(ct)} {verb}):")
                for c in ct:
                    print(c)
                total_ct += len(ct)
            for s in sr:
                print(s)
                total_sr += 1
            n_err += 1
            print()
        else:
            print(f"  ✅ {path.name}")

    print(f"\n{'='*65}")
    verb = '→ repariert' if fix else '→ mit --fix reparierbar'
    print(f"  Container-Fixes:   {total_ct}  {verb}")
    print(f"  Signalrot-Lücken:  {total_sr}  (manuell prüfen)")
    print(f"  Dateien betroffen: {n_err}")
    print(f"{'='*65}\n")

    if not fix and total_ct > 0:
        print("  → Tipp: python3 scripts/syntax_repair.py --fix\n")

    sys.exit(0 if total_ct == 0 else 1)


if __name__ == '__main__':
    main()
