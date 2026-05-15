import sys

def check_tables(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    in_table = False
    table_lines = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if '|' in stripped:
            if not in_table:
                in_table = True
                table_start = i + 1
            table_lines.append((i + 1, stripped))
        else:
            if in_table:
                validate_table(table_start, table_lines)
                in_table = False
                table_lines = []
    
    if in_table:
        validate_table(table_start, table_lines)

def validate_table(start_line, lines):
    print(f"Checking table starting at line {start_line}")
    col_counts = []
    for line_num, content in lines:
        # Simple count of pipes
        pipes = content.count('|')
        col_counts.append((line_num, pipes, content))
    
    if not col_counts:
        return

    # Check if header separator exists
    has_sep = any('---' in c[2] for c in col_counts)
    if not has_sep:
        # Might not be a standard GFM table, maybe a grid table or something else
        # But we mostly use GFM tables
        pass

    counts = [c[1] for c in col_counts]
    if len(set(counts)) > 1:
        print(f"  [!] Inconsistent pipe counts found in table at line {start_line}:")
        for line_num, count, content in col_counts:
            print(f"    Line {line_num:4}: {count} pipes | {content}")

if __name__ == "__main__":
    check_tables(sys.argv[1])
