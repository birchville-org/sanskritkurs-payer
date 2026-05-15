import os, re

bg_dir = "docs/bg/lektionen/"
critical = [
    re.compile(r'^# Lektion \d'),
    re.compile(r'^Bildung:$'),
    re.compile(r'^Maskulinum:$'),
    re.compile(r'^Femininum:$'),
    re.compile(r'^Neutrum:$'),
    re.compile(r'Übersetzen Sie'),
    re.compile(r'^Beachten Sie'),
    re.compile(r'^Zur Erklärung'),
    re.compile(r'^Den Großteil'),
    re.compile(r'^Dazu gehören'),
    re.compile(r'^Als Vorderglied'),
    re.compile(r'Abb\.:'),
    re.compile(r'Bildquelle:'),
    re.compile(r'^Selten vorkommend'),
    re.compile(r'^Das Femininum zu'),
    re.compile(r'^z\.B\.'),
    re.compile(r'^oder$'),
    re.compile(r'^Beispiele:$'),
    re.compile(r'^Rest wie'),
    re.compile(r'Public domain'),
]

damage = {}
for f in sorted(os.listdir(bg_dir)):
    if not f.endswith('.md'): continue
    path = bg_dir + f
    with open(path) as fh:
        for i, line in enumerate(fh, 1):
            for p in critical:
                if p.search(line):
                    if f not in damage: damage[f] = []
                    damage[f].append((i, line.rstrip()[:120]))
                    break

for f, hits in damage.items():
    print(f"\n=== {f} ({len(hits)} German lines) ===")
    for ln, text in hits:
        print(f"  L{ln}: {text}")

total = sum(len(h) for h in damage.values())
print(f"\nDAMAGE: {total} German-overwritten lines across {len(damage)} files")
