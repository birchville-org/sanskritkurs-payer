import os
import re

directory = 'docs/lektionen'
patterns = [
    re.compile(r'\n+---\n+Zu \[?Lektion.*$', re.DOTALL | re.IGNORECASE),
    re.compile(r'\n+Zu \[?Lektion.*$', re.DOTALL | re.IGNORECASE),
    re.compile(r'\n+Zu \[?Schriftübung.*$', re.DOTALL | re.IGNORECASE),
    re.compile(r'\n+Zu \[?Übung.*$', re.DOTALL | re.IGNORECASE),
    re.compile(r'\n+Zu \[?Lösung.*$', re.DOTALL | re.IGNORECASE),
    re.compile(r'\n+Zu den \[?Lösungen.*$', re.DOTALL | re.IGNORECASE),
]

for filename in os.listdir(directory):
    if filename.endswith('.md'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # We only want to remove it if it's near the end.
        # Let's check the last 200 characters.
        tail = content[-200:]
        for pattern in patterns:
            # We apply the pattern to the whole content but ensured it matches at the end ($)
            content = pattern.sub('', content)
        
        if content != original_content:
            print(f"Purged navigation links from {filename}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
