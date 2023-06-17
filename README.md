# VGTRE InShort

vgtree is a Python-based post-exploitation tool designed to assist ethical hackers and cybersecurity enthusiasts in their search for specific patterns/strings within the target system's files and directories. this tool i made can be also extends its search functionality within the output of system commands, mimicking the capabilities of traditional grep/find commands with a more user-friendly approach. while it doesnt replace them of-course, using it could be an extra thing.
While i thought using it for myself, i have decided to share it with the community in the hopes that it might be useful to others.
Even though the concept may not be new, i think others might find is a great tool.

![example](https://github.com/Adkali/vgtree/assets/90532971/7d8aa9f7-c100-41ca-b1e8-3cc9da91003a)


# Features
- Traverse directories recursively, inspecting each file for the desired pattern.
- Directly search using a pattern
- Search for a pattern within the output of a specified command
- using colors for better output

# Usage
<pre>
|  _____  | V
| |\ ___| | G
| | |   | | T
| | |___| | R
\ | |____\| E
 \|_________E
  v1.0

usage: tree.py [-h] [-d DIRECTORY] [-f FILE] [-e EXECUTE] -p PATTERN

options:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        Directory to search.
  -f FILE, --file FILE  File to search.
  -e EXECUTE, --execute EXECUTE
                        Search inside a command.
  -p PATTERN, --pattern PATTERN
                        Pattern/string/txt to search for.

</pre>

# Examples
- Searching for a pattern within a directory/file
<pre>python3 vgtree.py -d /path/to/directory -p search_string</pre>

-  Searching for a pattern within a file
<pre>python3 vgtree.py -f /path/to/file.txt -p search_string</pre>

