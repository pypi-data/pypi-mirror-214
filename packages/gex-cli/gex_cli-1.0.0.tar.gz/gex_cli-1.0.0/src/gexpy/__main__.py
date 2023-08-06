import sys

import click

from gexpy.cli import gex, commands


def main() -> click.Group:
    """CLI entry point."""
    for cmd in commands:
        gex.add_command(cmd)
    
    return gex()


if __name__ == '__main__':
    sys.exit(main())
