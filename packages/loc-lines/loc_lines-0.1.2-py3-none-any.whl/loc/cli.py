from argparse import ArgumentParser
from . import read

def main() -> None:
    parser: ArgumentParser = ArgumentParser(prog="LOC")
    parser.add_argument("path")
    parser.add_argument("-s", "--sub_search", action="store_true")
    parser.add_argument("-w", "--white_space", action="store_true")
    args, exts = parser.parse_known_args()
    read.read(args, exts)

if __name__ == "__main__":
    main()