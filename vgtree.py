import os
import argparse
import subprocess

# {MADE BY Adkali - GITHUB, LINKEDIN}
# {USE IT FOR EDUCATION PURPOSE ONLY.}
# {THIS 100+ LINES CODE CAN BE A POWERFULLY WEAPON WHEN IT COMES TO POST-EXPLOITATION.}
# {YOU CAN GATHER INFORMATION ABOUT THE SYSTEM.}
# {SEARCH FOR PATTERNS/STRINGS/WORDS/CLUES/VERSIONS/LEFT-NOTES OR/AND EVERYTHING YOU CAME-UP WITH.}
# {SEARCH THROUGH FILES - CHECK.}
# {SEARCH THROUGH DIRECTORIES - CHECK.}
# {INFORMATION OBTAINED CAN HELP IN THE NEXT STEPS.}
# {THIS TOOL ACTS LIKE THE GREP/FIND COMMANDS, BUT MAKING IT MORE NICE TO USE.}


# ----- PRINTING RESULTS WITH COLORS -----

def OutColors(text, color):
    colorQ = {
        'purple': '\033[95;1m', # Patterns Founds
        'blue': '\033[94m', # Directories
        'yellow': '\033[93;1m', # Founds Filesvgt
        'red': '\033[91;1m', # Error / Execute
        'end': '\033[0m', # End Of Colors
    }

    print(f"{colorQ[color]}{text}{colorQ['end']}")

Error = "Keep Moving..."
version = "1.0"

def Banner_Show():
    print(f'''
|  _____  | V
| |\ ___| | G
| | |   | | T
| | |___| | R
\ | |____\| E
 \|_________E
  v{version}
''')


parser = argparse.ArgumentParser(description=Banner_Show())
parser.add_argument('-d', '--directory', type=str, help='Directory to search.')
parser.add_argument('-f', '--file', type=str, help='File to search.')
parser.add_argument('-e', '--execute', type=str, help='Search inside a command.')
parser.add_argument('-p', '--pattern', type=str, required=True, help='Pattern/string/txt to search for.')
args = parser.parse_args()


# ----- DIRECTORIES, PATTERNS, COLORS -----

def FindGrep(root, pattern, color):
    for dir_path, dir_names, file_names in os.walk(root):
        # --- USE SPACES TO MAKE 'TREE' STRUCTURE.
        indent = "    " * (len(dir_path.split(os.sep)) - len(root.split(os.sep)))
        OutColors(f"{indent}│──{os.path.basename(dir_path)}", 'blue')
        for filename in file_names:
            file_path = os.path.join(dir_path, filename)
            try:
                with open(file_path, 'r', errors='ignore') as file:
                    lines = file.readlines()
                    for Newline in lines:
                        if pattern.lower() in Newline.lower():
                            OutColors(f"{indent}  │── {filename} <- Found Something", 'yellow')
                            print("")
                            OutColors(f"{indent}     └──  {Newline.strip()}", 'purple')
                            break
            except TypeError:
                pass
            except FileNotFoundError:
                OutColors(f"{indent}{Error}", "red")
            except OSError:
                continue


def main():
    if args.directory:
        FindGrep(args.directory, args.pattern, 'purple')
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if args.pattern.lower() in line.lower():
                        OutColors(line.strip(), 'purple')
        except IsADirectoryError:
            print(f"{args.file} is a directory!")
            print("Use '-f' on the specific file if you want to find pattern.")
    elif args.execute:
        command_output = subprocess.run(args.execute, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        cmd = command_output.split('\n')
        for line in cmd:
            if args.pattern.lower() in line.lower():
                OutColors(line.strip(), 'red')
    else:
        FindGrep(os.getcwd(), args.pattern, 'purple')


if __name__ == '__main__':
    main()