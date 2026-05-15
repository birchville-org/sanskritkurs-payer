import os

def fix_script_tags(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '<script setup>' in content and '</script>' not in content:
        # Append </script> at the end or after the block
        content += '\n</script>\n'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_script_tags(os.path.join(root, filename))

print("Script tags stabilized.")
