import sys
import re

def restore_file(de_path, bg_path):
    with open(de_path, "r", encoding="utf-8") as f:
        de_content = f.read()
    with open(bg_path, "r", encoding="utf-8") as f:
        bg_content = f.read()

    # Strategy: Replace Devanagari blocks in BG with those from DE
    # A Devanagari block is often a table row or a list item.
    
    # Let's target table rows specifically: | ... | ... |
    de_rows = re.findall(r'\|.*\|', de_content)
    bg_rows = re.findall(r'\|.*\|', bg_content)
    
    # This is risky if the number of rows doesn't match.
    # A better way: find strings that contain Devanagari in DE and find their 'corrupted' counterpart in BG.
    
    # Let's use a simpler approach for the pilot: 
    # Find all strings in BG that contain a mix of Devanagari and Cyrillic.
    mixed_strings = re.findall(r'[अ-ह][\u0400-\u04FF]+[अ-ह]*|[\u0400-\u04FF]+[अ-ह]+[\u0400-\u04FF]*', bg_content)
    
    # For each mixed string, we need to find the correct Devanagari in DE.
    # This is hard. 
    
    # ALTERNATIVE: Re-generate the tables by taking the DE table structure and applying BG header translations.
    
    # Let's try to find table blocks.
    de_tables = re.findall(r'(\|(?:.*\|)+\n(?:\|(?:[-:| ]+)\|)+\n(?:\|(?:.*\|)+\n)+)', de_content)
    bg_tables = re.findall(r'(\|(?:.*\|)+\n(?:\|(?:[-:| ]+)\|)+\n(?:\|(?:.*\|)+\n)+)', bg_content)
    
    if len(de_tables) == len(bg_tables):
        for i in range(len(de_tables)):
            # We want to keep the Bulgarian headers but use the German body.
            de_lines = de_tables[i].splitlines()
            bg_lines = bg_tables[i].splitlines()
            
            # Rebuild table: Use BG headers (first 1-2 lines), use DE body (from line 2 or 3)
            # Find the separator line index
            sep_idx = 0
            for j, line in enumerate(de_lines):
                if re.match(r'\|[-:| ]+\|', line):
                    sep_idx = j
                    break
            
            new_table_lines = bg_lines[:sep_idx+1] + de_lines[sep_idx+1:]
            new_table = "\n".join(new_table_lines) + "\n"
            bg_content = bg_content.replace(bg_tables[i], new_table)
            
    with open(bg_path, "w", encoding="utf-8") as f:
        f.write(bg_content)

if __name__ == "__main__":
    restore_file("/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion27.md", "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/lektion27.md")
    print("Restored lektion27.md tables")
