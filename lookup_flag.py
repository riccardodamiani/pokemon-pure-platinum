#!/usr/bin/env python3
"""Look up a flag/var name in generated/vars_flags.txt and print its line number and ID."""

import sys
import os


def load_symbols(filename):
    """Parse vars_flags.txt and return a dict of name -> (id, line_number).

    Rules:
      - Plain NAME:           id = counter, counter++
      - NAME = OTHER_NAME:    id = OTHER_NAME's id, counter unchanged
      - NAME = NUMBER:        id = NUMBER,   counter = NUMBER + 1
    """
    symbols = {}
    counter = 0

    with open(filename) as f:
        lines = f.readlines()

    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue

        if '=' in stripped:
            lhs, rhs = stripped.split('=', 1)
            name  = lhs.strip()
            value = rhs.strip()

            # Try numeric literal (decimal or hex)
            try:
                literal = int(value, 0)
                current_id = literal
                counter = literal + 1
            except ValueError:
                # Reference to another symbol
                current_id = symbols[value][0] if value in symbols else counter
                # counter is NOT updated for name-references

        else:
            name = stripped
            current_id = counter
            counter += 1

        symbols[name] = (current_id, line_num)

    return symbols


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <symbol_name>", file=sys.stderr)
        sys.exit(1)

    search = sys.argv[1]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(script_dir, 'generated', 'vars_flags.txt')

    if not os.path.exists(filename):
        print(f"Error: {filename} not found", file=sys.stderr)
        sys.exit(1)

    symbols = load_symbols(filename)

    if search not in symbols:
        print(f"'{search}' not found", file=sys.stderr)
        sys.exit(1)

    sym_id, line_num = symbols[search]
    print(f"Line {line_num}: {search} = 0x{sym_id:04X} ({sym_id})")


if __name__ == '__main__':
    main()
