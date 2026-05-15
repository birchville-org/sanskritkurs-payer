import os
import re

directory = 'docs/public/qa'
script_tag = """
<script>
  // Sync-Funkspruch an den Viewer
  window.addEventListener('scroll', () => {
    window.parent.postMessage({
      type: 'scroll',
      pct: window.scrollY / (document.documentElement.scrollHeight - window.innerHeight),
      top: window.scrollY,
      id: window.name || 'left-frame'
    }, '*');
  });
  // Empfange Funkspruch vom Viewer
  window.addEventListener('message', (e) => {
    if (e.data.type === 'setScroll') {
       window.scrollTo({ top: e.data.top, behavior: 'auto' });
    }
  });
</script>
"""

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'window.parent.postMessage' not in content:
            # Füge das Skript vor dem schließenden Body-Tag ein
            new_content = content.replace('</body>', script_tag + '</body>')
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
