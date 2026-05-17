import os
import re

def check_tables(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_table = False
    table_lines = []
    errors = []
    
    for i, line in enumerate(lines):
        if '|' in line:
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append((i + 1, line))
        else:
            if in_table:
                # End of table, validate it
                if len(table_lines) > 1:
                    # Count pipes in each line (excluding escaped ones maybe, but simple count first)
                    counts = [l.count('|') for _, l in table_lines]
                    # Filter out the separator line (usually has many | but it must match header)
                    # Actually, all lines in a valid markdown table must have the same structure
                    if len(set(counts)) > 1:
                        # Check if it's just the separator line being weird or a real mismatch
                        # Actually, commonmark/gfm requires same column count
                        # We ignore lines that are clearly not part of the table body/header if they just happen to have a pipe
                        # but usually in this project they are strict.
                        errors.append(f"Table at lines {table_lines[0][0]}-{table_lines[-1][0]} has mismatched columns: {counts}")
                in_table = False
    
    return errors

lektionen_dir = 'docs/lektionen'
for filename in os.listdir(lektionen_dir):
    if filename.endswith('.md'):
        path = os.path.join(lektionen_dir, filename)
        errs = check_tables(path)
        if errs:
            print(f"File: {path}")
            for e in errs:
                print(f"  {e}")
