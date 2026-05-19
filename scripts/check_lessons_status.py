import os
import re

print("| Lesson | Status | Last Reconstructed | Has TODOs? |")
print("|--------|--------|---------------------|------------|")

for i in range(1, 62):
    filename = f"lektion{i:02d}.md"
    filepath = os.path.join("docs", "lektionen", filename)
    if not os.path.exists(filepath):
        print(f"| Lektion {i:02d} | ❌ MISSING | - | - |")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Parse frontmatter
    status = "-"
    last_recon = "-"
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if frontmatter_match:
        fm_text = frontmatter_match.group(1)
        status_match = re.search(r"status:\s*\"?([^\n\"]+)\"?", fm_text)
        if status_match:
            status = status_match.group(1)
        recon_match = re.search(r"last_reconstructed:\s*\"?([^\n\"]+)\"?", fm_text)
        if recon_match:
            last_recon = recon_match.group(1)
            
    # Search for common TODO markers or placeholders
    has_todos = "No"
    if "TODO" in content or "FIXME" in content or "placeholder" in content.lower():
        has_todos = "⚠️ Yes"
        
    print(f"| Lektion {i:02d} | {status} | {last_recon} | {has_todos} |")
