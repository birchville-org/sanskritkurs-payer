import os
import subprocess
import glob

IMAGE_DIR = "docs/public/images"
DOCS_DIR = "docs"
SIZE_THRESHOLD = 50 * 1024 # 50KB

def optimize_images():
    images = []
    for ext in ('*.jpg', '*.jpeg', '*.png'):
        images.extend(glob.glob(os.path.join(IMAGE_DIR, ext)))

    converted = {}

    print(f"Found {len(images)} total images. Checking for sizes > 50KB...")

    for img in images:
        size = os.path.getsize(img)
        if size > SIZE_THRESHOLD:
            base, ext = os.path.splitext(img)
            webp_path = base + ".webp"
            # If we already converted it in a previous run, skip cwebp but record it
            if not os.path.exists(webp_path):
                cmd = ["cwebp", "-q", "80", img, "-o", webp_path]
                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    converted[os.path.basename(img)] = os.path.basename(webp_path)
                    print(f"Converted {img} to WebP.")
                except subprocess.CalledProcessError as e:
                    print(f"Failed to convert {img}: {e}")
            else:
                converted[os.path.basename(img)] = os.path.basename(webp_path)

    print(f"Converted {len(converted)} images. Updating markdown files...")

    # Update markdown files
    md_files = glob.glob(os.path.join(DOCS_DIR, "**/*.md"), recursive=True)
    updated_files = 0

    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content
        for old_img, new_img in converted.items():
            new_content = new_content.replace(f"/images/{old_img}", f"/images/{new_img}")
            # handle cases where the leading slash might be missing
            new_content = new_content.replace(f"](images/{old_img})", f"](images/{new_img})")

        if content != new_content:
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            updated_files += 1

    print(f"Updated {updated_files} markdown files.")

if __name__ == "__main__":
    optimize_images()
