# loc-lines

Lines Of Code is a command-line tool that tells you how many lines a file or children of a directory have.

## Installation

```shell
pip install loc-lines
```

## Usage

To read a file, simply use the command:
```shell
py -m loc \path\to\file
```
Want to include whitespace in the response?:
```shell
py -m loc \path\to\file -w
```

To read a directory filled with files do:
```shell
py -m loc \path\to\dir .txt .py
```
The trailing file extensions specify which extensions to include in your response.
Ex. If a directory has three files, a .txt, a .py, and a .java, lines will only be read from the first two.

To search all sub directory's:
```shell
py -m loc \path\to\dir -s .txt .py
```
Specify the option -s to search all sub directory's of the selected directory