#!/usr/bin/env python
from sentweement.commands import base

import sys

def main(args):
    prog_name = args[0]

    try:
        command = args[1]
    except IndexError:
        command = "help"

    return base.run_command(prog_name, command, args[2:])

if __name__ == "__main__":
    sys.exit(main(sys.argv))
