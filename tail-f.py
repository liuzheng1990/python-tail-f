"""
        tail-f.py

A script which works like `tail -f` on Unix. It's a useful tool for
monitoring logs in real-time.
    
Usage:

    ``tail-f <txt file path> [line_number]``

#. At the start, the last `line_number` lines will be displayed on the screen.
If `line_number` not given, its default value is 10.

#. If new content went into the text file, new text will be displayed
on the screen.

#. If the previous content changed, a warning message will be displayed
on the screen, and then the program will track the change from the new file.
Old content will be discarded. The entire text file will be displayed after the
warning message.
"""
CHECK_PERIOD = 0.1 # check every 0.1s

import sys
import time

################################################################################
#           helper functions
################################################################################
def get_start_idx_last_lines(s_full, n=0):
    """
    Get the starting index of `s_full` for the last `n` lines.

    If n <= 0 (default), returns -1.
    """
    if n <= 0:
        return -1
    idx = len(s_full) # points to the last character of `s_full`.
    while n > 0 and idx >= 0:
        idx = s_full.rfind('\n', 0, idx)
        n -= 1
    if idx < 0:
        idx = -1
    return idx

################################################################################
#               workflow
################################################################################

# parse args
if len(sys.argv) < 2:
    print("Usage: tail-f <text file path>", file=sys.stderr)
    exit(1)
input_fn = sys.argv[1]
line_number = 10
if len(sys.argv) > 2: # optional `line_number`
    line_number = int(sys.argv[2])
    if line_number < 0:
        line_number = 10

# Initial display
current_content = open(input_fn, 'r').read()
idx = get_start_idx_last_lines(current_content, line_number)
sys.stdout.write(current_content[idx+1:])
sys.stdout.flush()

try:
    while True:
        new_content = open(input_fn, 'r').read()
        if new_content.startswith(current_content):
            sys.stdout.write(new_content[len(current_content):])
            sys.stdout.flush()
            current_content = new_content
        else:
            print(
                '\n' + "*"*6 + \
                "WARNING: Previous content changed! Reload last {} lines.".format(line_number) + \
                "*"*6
            )
            current_content = new_content
            idx = get_start_idx_last_lines(current_content, line_number)
            sys.stdout.write(current_content[idx+1:])
            sys.stdout.flush()
        time.sleep(CHECK_PERIOD)
except KeyboardInterrupt:
    exit(0)





    