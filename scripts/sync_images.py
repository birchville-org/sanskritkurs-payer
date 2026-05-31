"""
sync_images.py — Sync image links from German lektion files to all locale copies.

Usage:
  python3 scripts/sync_images.py          # sync all lektionen
  python3 scripts/sync_images.py 15       # sync lektion 15 only
  python3 scripts/sync_images.py 6 12 42  # sync specific lektionen
"""

import os
import re
import sys


def sync_image_links(lesson_nums=None):
    root_dir = 'docs/lektionen'
    locales = [
        'bg', 'it', 'en', 'es', 'ru', 'uk', 'hi', 'fr', 'rm', 'ta',
        'ar', 'arc', 'he', 'zh', 'la', 'grc', 'el', 'fa', 'akk', 'cop',
    ]

    if lesson_nums is not None:
        files = [f"lektion{n:02d}.md" for n in lesson_nums]
    else:
        files = sorted(f for f in os.listdir(root_dir) if f.endswith('.md'))

    for file in files:
        root_path = os.path.join(root_dir, file)
        if not os.path.exists(root_path):
            print(f"  {file}: not found, skipping")
            continue

        with open(root_path, 'r', encoding='utf-8') as f:
            root_content = f.read()

        # Extract all image links in order
        root_images = re.findall(r'!\[.*?\]\((/images/.*?)\)', root_content)

        for locale in locales:
            locale_path = os.path.join('docs', locale, 'lektionen', file)
            if not os.path.exists(locale_path):
                continue

            with open(locale_path, 'r', encoding='utf-8') as f:
                locale_content = f.read()

            # Find all image links in locale file
            locale_images = re.findall(r'!\[.*?\]\((/images/.*?)\)', locale_content)

            if len(root_images) == len(locale_images):
                new_locale_content = locale_content
                for root_img, loc_img in zip(root_images, locale_images):
                    if root_img != loc_img:
                        print(f"Syncing image: {loc_img} -> {root_img} in {locale_path}")
                        new_locale_content = new_locale_content.replace(loc_img, root_img)

                if new_locale_content != locale_content:
                    with open(locale_path, 'w', encoding='utf-8') as f:
                        f.write(new_locale_content)
            else:
                print(f"Warning: Image count mismatch in {locale_path} ({len(locale_images)} vs {len(root_images)})")
                # Fallback: fix obvious corruptions like lekt0_01
                fixed_content = re.sub(r'/images/lekt(\d)_(\d+)\.jpg', lambda m: f'/images/lekt0{m.group(1)}{m.group(2)}.jpg', locale_content)
                fixed_content = re.sub(r'/images/ue[ऀ-৿]+ung', '/images/uebung', fixed_content)
                if fixed_content != locale_content:
                    with open(locale_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 scripts/sync_images.py <all|lesson_num [...]>")
        print("Example: python3 scripts/sync_images.py all")
        print("Example: python3 scripts/sync_images.py 15")
        print("Example: python3 scripts/sync_images.py 6 12 42")
        sys.exit(1)
    if args[0].lower() == "all":
        lesson_nums = None
    else:
        lesson_nums = []
        for a in args:
            try:
                lesson_nums.append(int(a))
            except ValueError:
                print(f"Warning: ignoring non-numeric argument '{a}'")

    sync_image_links(lesson_nums)


if __name__ == '__main__':
    main()
