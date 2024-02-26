import select
import sys


def listen_for_input():
    """Check for user input without blocking the loop."""
    rlist, _, _ = select.select([sys.stdin], [], [], 0)
    if rlist:
        user_input = sys.stdin.readline().strip()
        if user_input.lower() == 'q' or user_input.lower() == 'quit':
            exit()
