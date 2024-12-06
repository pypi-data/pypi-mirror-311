import sys
import os
import string
from argparse import Namespace

def path_exts(path: str) -> bool:
    return os.path.exists(path)

def get_ext(file: str) -> str:
    return os.path.splitext(file)[1]

def get_dir(dir: str, sub: bool, exts: tuple[str]) -> list[str]:
    files: list[str] = list()

    for file in os.listdir(dir):
        full_path: str = os.path.join(dir, file)
        
        if os.path.isdir(full_path) and sub: #If sub search is enabled and the current file is a directory
            for sub_file in get_dir(full_path, True, exts): #Recursively search all directorys
                full_file_path: str = os.path.join(full_path, sub_file)
                files.append(full_file_path)
            continue

        if get_ext(file) in exts:
            files.append(full_path)

    return files

def get_lines(file_path: str, ws: bool) -> int:
    with open(file_path) as f:
        lines: list[str] = f.readlines()
        lines_nws: int = len([line for line in lines if not all(char in string.whitespace for char in line)])
        lines_n: int = len(lines)
         
        if ws:
            return lines_n
        else:
            return lines_nws

def ws_text(ws: bool) -> str:
    ws_text: str = ""

    if ws:
        ws_text = "with"
    else:
        ws_text = "without"

    return ws_text

def read_dir(dir: str, sub: bool, ws: bool, exts: list[str]) -> None:
    if not path_exts(dir): sys.exit("Directory does not exist!")

    #Get files in directory
    files: list[str] = get_dir(dir, sub, exts)
    file_lines: dict[str, int] = {}

    for file in files:
        base_name: str = os.path.basename(file)
        lines: int = get_lines(file, ws)
        file_lines[base_name] = lines
    
    for file, lines in file_lines.items():
        print(f"File '{file}' has {lines} lines {ws_text(ws)} whitespace.")

    total_lines: int = 0
    for count in file_lines.values():
        total_lines += count

    print(f"In total that is {total_lines} lines in the directory {dir}")

def read_file(file: str, ws: bool) -> None:
    lines: int = get_lines(file, ws)
    base_name: str = os.path.basename(file)

    print(f"File '{base_name}' has {lines} lines {ws_text(ws)} whitespace.")

def read(args: Namespace, exts: list) -> None:
    if not path_exts(args.path): sys.exit("Provided path doesnt exist")
    if os.path.isfile(args.path) and args.sub_search: sys.exit("Cannot apply sub_search on a file, only a directory")

    if os.path.isdir(args.path):
        read_dir(args.path, args.sub_search, args.white_space, exts)
    if os.path.isfile(args.path):
        read_file(args.path, args.white_space)