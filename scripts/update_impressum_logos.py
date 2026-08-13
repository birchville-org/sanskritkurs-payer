import glob
import re

cc_button_regex = r'\[!\[CC BY-SA 4\.0\]\(https://licensebuttons\.net/l/by-sa/4\.0/80x15\.png\)\]\(https://creativecommons\.org/licenses/by-sa/4\.0/\)\s*'

github_logo_html = ' [<img src="/images/github.svg" alt="GitHub" class="inline-icon" />](https://github.com/birchville-org/sanskritkurs-payer)'
birchville_logo_html = ' [<img src="/birchville_logo.png" alt="Birchville" class="inline-icon" style="height: 1.35em !important;" />](https://birchville.cc)'

updated_files = 0
for filepath in glob.glob('/Volumes/SanDisk1TB/proj/Payer/docs/**/impressum.md', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove CC logo badge image if present
    content = re.sub(cc_button_regex, '', content)

    # 2. Clean previous github & birchville logo injections to re-inject cleanly
    content = re.sub(r'\s*\[<img src="/images/github\.svg"[^>]*>\]\(https://github\.com/(?:marcodem|birchville-org)/sanskritkurs-payer\)', '', content)
    content = re.sub(r'\s*\[<img src="/birchville_logo\.png"[^>]*>\]\(https://birchville\.cc\)', '', content)

    # 3. Inject GitHub logo with exactly 1 space behind MIT License link
    content, c1 = re.subn(
        r'(\[MIT License\]\(https://opensource\.org/licenses/MIT\)|MIT License|MIT)',
        r'\1' + github_logo_html,
        content,
        count=1
    )

    # 4. Inject Birchville logo slightly larger with 1 space behind Hrsg. (or ed./éd./a cura di etc.)
    def replace_demarmels(match):
        inner = match.group(1).rstrip()
        return f'Marco Demarmels ({inner}{birchville_logo_html})'

    content, c2 = re.subn(
        r'Marco Demarmels \(([^)]+)\)',
        replace_demarmels,
        content,
        count=1
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    updated_files += 1

print(f"Successfully updated logo formatting in {updated_files} impressum.md files.")
