import re

def load_file(file_path):
    """Loads a file and returns its lines."""
    with open(file_path, 'r') as file:
        return file.readlines()

def save_file(file_path, lines):
    """Saves lines to a file."""
    with open(file_path, 'w') as file:
        file.writelines(lines)

def parse_cpplinter(cpplinter_lines):
    """Parses cpplinter.lua to extract keys and their associated source lines."""
    table = {}
    pattern_key = re.compile(r'^---\*\s*(.+)')  # Matches lines starting with "---*"
    pattern_source = re.compile(r'^---@source\s+(.+):(\d+)')  # Matches lines starting with "@source"

    i = 0
    while i < len(cpplinter_lines):
        key_match = pattern_key.match(cpplinter_lines[i])
        if key_match:
            key = key_match.group(1).strip()  # Remove the "---*" prefix
            if i + 1 < len(cpplinter_lines):
                source_match = pattern_source.match(cpplinter_lines[i + 1])
                if source_match:
                    file_path = source_match.group(1).strip()
                    line_number = int(source_match.group(2).strip())
                    table[key] = (file_path, line_number)
        i += 1

    return table

def verify_and_update_table(table, luascript_lines):
    """Verifies and updates the table with the correct line numbers."""
    updated_table = {}
    for key, (file_path, line_number) in table.items():
        if line_number <= len(luascript_lines):
            # Verify the line content matches the key
            if key in luascript_lines[line_number - 1]:
                updated_table[key] = (file_path, line_number)
            else:
                # Search for the correct line number
                for i, line in enumerate(luascript_lines):
                    if key in line:
                        updated_table[key] = (file_path, i + 1)
                        break
        else:
            # Search for the correct line number
            for i, line in enumerate(luascript_lines):
                if key in line:
                    updated_table[key] = (file_path, i + 1)
                    break

    return updated_table

def update_cpplinter(cpplinter_lines, table):
    """Updates cpplinter.lua lines with the new line numbers."""
    pattern_key = re.compile(r'^---\*\s*(.+)')
    pattern_source = re.compile(r'^---@source\s+(.+):(\d+)')

    updated_lines = []
    i = 0
    while i < len(cpplinter_lines):
        key_match = pattern_key.match(cpplinter_lines[i])
        if key_match:
            key = key_match.group(1).strip()
            if key in table:
                file_path, new_line_number = table[key]
                updated_lines.append(f"---*{key}\n")  # Add back the "---*" prefix
                updated_lines.append(f"---@source {file_path}:{new_line_number}\n")  # Update the source line
                i += 2  # Skip the next line since it's being replaced
                continue
        updated_lines.append(cpplinter_lines[i])
        i += 1

    return updated_lines

def main():
    # File paths
    cpplinter_path = 'cpplinter.lua'
    luascript_path = 'luascript.cpp'

    # Load files
    cpplinter_lines = load_file(cpplinter_path)
    luascript_lines = load_file(luascript_path)

    # Parse cpplinter.lua
    table = parse_cpplinter(cpplinter_lines)

    # Verify and update table
    updated_table = verify_and_update_table(table, luascript_lines)

    # Update cpplinter.lua
    updated_cpplinter_lines = update_cpplinter(cpplinter_lines, updated_table)

    # Save the updated cpplinter.lua
    save_file(cpplinter_path, updated_cpplinter_lines)

if __name__ == '__main__':
    main()