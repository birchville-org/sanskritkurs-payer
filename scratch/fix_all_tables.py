import sys
import re

def fix_all_tables(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_table = False
    table_lines = []

    for line in lines:
        stripped = line.strip()
        # Detect table line (starts with | or > |)
        if stripped.startswith('|') or stripped.startswith('> |'):
            in_table = True
            # Clean the line: remove leading "> ", remove trailing spaces
            clean_line = stripped.lstrip('> ').rstrip()
            # If line starts with |, keep it. If it doesn't, it's a broken multiline cell
            if not clean_line.startswith('|'):
                 # Join with previous row's last cell if possible, or just fix it
                 if table_lines:
                     prev = table_lines[-1]
                     # Remove trailing pipe from previous if it exists
                     if prev.endswith('|'):
                         table_lines[-1] = prev[:-1] + " [[br]] " + clean_line + " |"
                     else:
                         table_lines[-1] = prev + " [[br]] " + clean_line
                 continue
            table_lines.append(clean_line)
        else:
            if in_table:
                # Close table
                new_lines.append("::: grammar-box\n")
                for tl in table_lines:
                    # Ensure it ends with |
                    if not tl.endswith('|'):
                        tl += " |"
                    new_lines.append(tl + "\n")
                new_lines.append(":::\n")
                in_table = False
                table_lines = []
            new_lines.append(line)

    if in_table:
        new_lines.append("::: grammar-box\n")
        for tl in table_lines:
            if not tl.endswith('|'):
                tl += " |"
            new_lines.append(tl + "\n")
        new_lines.append(":::\n")

    # Second pass: fix header separators and column counts
    final_lines = []
    i = 0
    while i < len(new_lines):
        line = new_lines[i]
        if line == "::: grammar-box\n":
            final_lines.append(line)
            i += 1
            table_content = []
            while i < len(new_lines) and new_lines[i] != ":::\n":
                table_content.append(new_lines[i])
                i += 1
            
            # Fix table_content
            if table_content:
                # Find max columns
                max_cols = 0
                for row in table_content:
                    max_cols = max(max_cols, row.count('|') - 1)
                
                fixed_content = []
                for row in table_content:
                    cols = row.count('|') - 1
                    if cols < max_cols:
                        # Append empty cells
                        row = row.rstrip('\n').rstrip('|') + (" |" * (max_cols - cols)) + " |\n"
                    fixed_content.append(row)
                
                final_lines.extend(fixed_content)
            
            if i < len(new_lines):
                final_lines.append(new_lines[i])
                i += 1
        else:
            final_lines.append(line)
            i += 1

    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

if __name__ == "__main__":
    fix_all_tables(sys.argv[1])
