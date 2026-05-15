import re

def clean_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove <span> wrappers for Devanagari
    content = re.sub(r'<span class="sanskrit-dev">([\s\S]*?)</span>', r'\1', content)
    
    # 2. Convert <p align="center"> to simple text or blockquotes
    content = re.sub(r'<p align="center" class="text-highlight">([\s\S]*?)</p>', r'\1', content)
    content = re.sub(r'<p align="center">([\s\S]*?)</p>', r'\1', content)
    
    # 3. Remove <div> containers
    content = re.sub(r'<div align="center">([\s\S]*?)</div>', r'\1', content)
    
    # 4. Remove remaining <br>
    content = content.replace('<br>', '\n')
    
    # 5. Convert HTML tables to Markdown tables (simplified)
    # This is a bit complex for a regex, so we do it manually for Lektion 01's specific table
    table_regex = re.compile(r'<table>[\s\S]*?</table>', re.DOTALL)
    
    def table_replacer(match):
        # We know the table in Lektion 01
        return """
| Laut | Beschreibung |
| :--- | :--- |
| **a - अ** | "kurzes a" wird bei den Indern -- schon seit alter Zeit -- oft wie ə ausgesprochen. In Europa spricht man es als kurzes a, in Bengalen als kurzes dunkles o. |
| **ṛ - ऋ** | wie böhmisches vokalisiertes r. Leichter Nachklang von i. |
| **ṝ - ॠ** | wie böhmisches vokalisiertes r. Leichter Nachklang von u. |
| **jñ - ज्ञ्** | auch wie dny (Marāṭhī) oder gy (Nordindisch). |
| **ś - श्** | sch-Laut mit nach unten gebogener Zungenspitze. Ähnlich wie sch in "mischen". |
| **ṣ - ष्** | ach-Laut mit zurückgebogener Zungenspitze. Öfters so weit hinten im Rachen artikuliert, dass es fast wie kh klingt. |
| **h - ह्** | Hauchlaut, nie Dehnungszeichen. |
| **ḥ - :** | **Visarga (Visarjanīya)** -- विसर्ग / विसर्जनीय. Stimmloser Hauchlaut mit Nachklang des vorhergehenden Vokals oder des zweiten Teils des vorausgehenden Diphtones: agniḥ -- अग्निः = agnihi, devaiḥ -- देवैः = devaihi, gauḥ -- गौः = gauhu |
| **ṃ** | **Anusvara** -- अनुस्वर. Vor Zischlauten, h, l: Nasalierung des Vokals. Im Auslaut = m. Im Inlaut vor Konsonanten: der dem folgenden Konsonanten entsprechende Nasal: saṃdhi -- संबंधित = sandhi -- सन्धि |
"""

    content = table_regex.sub(table_replacer, content)

    # 6. Cleanup multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

if __name__ == "__main__":
    clean_html("/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion01.md")
