import os
import argparse
import subprocess
import re

# {MADE BY Adkali - GITHUB, LINKEDIN}
# {USE IT FOR EDUCATION PURPOSE ONLY.}
# {THIS TOOL IS INTENDED FOR POST-EXPLOITATION INFORMATION GATHERING.}
# {IT ACTS SIMILAR TO GREP/FIND, BUT OFFERS IMPROVED OUTPUT OPTIONS.}

# ----- PRINTING RESULTS WITH COLORS -----

def out_colors(text, color):
    color_codes = {
        'purple': '\033[95;1m',  # Patterns Found
        'blue': '\033[94m',      # Directories
        'yellow': '\033[93;1m',  # Found Files
        'red': '\033[91;1m',     # Error / Command Output
        'end': '\033[0m'         # Reset Color
    }
    print(f"{color_codes.get(color, '')}{text}{color_codes['end']}")

ERROR_MSG = "Keep Moving..."
VERSION = "1.1"

def banner_show():
    print(f'''
|  _____  | V
| |\ ___| | G
| | |   | | T
| | |___| | R
\ | |____\| E
 \|_________E
  v{VERSION}
''')

def search_in_file(file_path, pattern, regex=False, line_numbers=False, context=0):
    """
    Search for a pattern in a file.
    Returns a list of tuples: (line_number, [context_lines]) for each match.
    """
    matches = []
    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                found = False
                if regex:
                    if re.search(pattern, line, re.IGNORECASE):
                        found = True
                else:
                    if pattern.lower() in line.lower():
                        found = True
                if found:
                    start = max(0, idx - context)
                    end = min(len(lines), idx + context + 1)
                    context_lines = lines[start:end]
                    matches.append((idx + 1, context_lines))
    except Exception as e:
        out_colors(f"Error reading {file_path}: {str(e)}", "red")
    return matches

def find_grep(root, pattern, regex, line_numbers, context):
    """
    Recursively search through directories and files under 'root'
    for the specified pattern.
    """
    for dir_path, dir_names, file_names in os.walk(root):
        # Use spaces for a tree-like structure based on directory depth
        indent = "    " * (len(dir_path.split(os.sep)) - len(root.split(os.sep)))
        out_colors(f"{indent}│── {os.path.basename(dir_path)}", 'blue')
        for filename in file_names:
            file_path = os.path.join(dir_path, filename)
            matches = search_in_file(file_path, pattern, regex, line_numbers, context)
            if matches:
                out_colors(f"{indent}  │── {filename} <- Found Something", 'yellow')
                for line_num, context_lines in matches:
                    # Print each context line; if line_numbers enabled, approximate numbers are shown.
                    for i, context_line in enumerate(context_lines):
                        # Calculate a rough line number for context display
                        display_line = (line_num - (len(context_lines) // 2)) + i
                        if line_numbers:
                            out_colors(f"{indent}     └── [{display_line}] {context_line.strip()}", 'purple')
                        else:
                            out_colors(f"{indent}     └── {context_line.strip()}", 'purple')
                print("")  # Extra newline for clarity

def search_in_file_single(file_path, pattern, regex, line_numbers, context):
    """
    Search a specific file and print matches directly.
    """
    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                found = False
                if regex:
                    if re.search(pattern, line, re.IGNORECASE):
                        found = True
                else:
                    if pattern.lower() in line.lower():
                        found = True
                if found:
                    if line_numbers:
                        out_colors(f"[{idx+1}] {line.strip()}", 'purple')
                    else:
                        out_colors(line.strip(), 'purple')
    except Exception as e:
        out_colors(f"Error reading {file_path}: {str(e)}", "red")

def execute_and_search(command, pattern, regex, line_numbers, context):
    """
    Execute a shell command, capture its output, and search for the pattern.
    """
    command_output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
    lines = command_output.splitlines()
    for idx, line in enumerate(lines):
        found = False
        if regex:
            if re.search(pattern, line, re.IGNORECASE):
                found = True
        else:
            if pattern.lower() in line.lower():
                found = True
        if found:
            if line_numbers:
                out_colors(f"[{idx+1}] {line.strip()}", 'red')
            else:
                out_colors(line.strip(), 'red')

def main():
    banner_show()
    parser = argparse.ArgumentParser(
        description="Search for a pattern in files, directories, or command output.\n"
                    "Enhanced with regex support, line numbers, and context options."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--directory', type=str, help='Directory to search.')
    group.add_argument('-f', '--file', type=str, help='File to search.')
    group.add_argument('-e', '--execute', type=str, help='Command to execute and search its output.')
    parser.add_argument('-p', '--pattern', type=str, required=True, help='Pattern/string/text to search for.')
    parser.add_argument('--regex', action='store_true', help='Treat the pattern as a regular expression.')
    parser.add_argument('--line-numbers', action='store_true', help='Display line numbers in the output.')
    parser.add_argument('--context', type=int, default=0, help='Show additional context lines before and after each match (default: 0).')
    args = parser.parse_args()

    if args.directory:
        find_grep(args.directory, args.pattern, args.regex, args.line_numbers, args.context)
    elif args.file:
        search_in_file_single(args.file, args.pattern, args.regex, args.line_numbers, args.context)
    elif args.execute:
        execute_and_search(args.execute, args.pattern, args.regex, args.line_numbers, args.context)
    else:
        find_grep(os.getcwd(), args.pattern, args.regex, args.line_numbers, args.context)

if __name__ == '__main__':
    main()
