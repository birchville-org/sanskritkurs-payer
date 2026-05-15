import os
import re

def add_qa_to_locale(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'link: \'/qa_viewer.html\'' in content:
        return # Already added
    
    # Insert before the last item in the nav array or before Impressum/Contact
    # More robust: find the 'nav: [' block
    nav_match = re.search(r'nav:\s*\[(.*?)\s*\]', content, re.DOTALL)
    if nav_match:
        nav_content = nav_match.group(1)
        # Add before the last entry (usually Impressum or similar)
        lines = nav_content.split('\n')
        # Find index of last meaningful line (non-empty)
        last_idx = -1
        for i in range(len(lines)-1, -1, -1):
            if '{' in lines[i]:
                last_idx = i
                break
        
        if last_idx != -1:
            lines.insert(last_idx, "      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },")
            new_nav = '\n'.join(lines)
            content = content.replace(nav_content, new_nav)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added QA to {filepath}")

def main():
    locales_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/locales"
    for filename in os.listdir(locales_dir):
        if filename.endswith(".mjs"):
            add_qa_to_locale(os.path.join(locales_dir, filename))

if __name__ == "__main__":
    main()
