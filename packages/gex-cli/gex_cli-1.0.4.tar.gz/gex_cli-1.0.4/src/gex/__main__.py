import sys
from .cli import gex, g, _list


def main():
    gex.add_command(g)
    gex.add_command(_list)
    
    return gex()


if __name__ == '__main__':
    sys.exit(main())
