import os
import csv
from pathlib import Path
import sys

os.chdir('..')
# base_path = os.getcwd()
base_path = "C:\\Users\\pabst\\OneDrive\\Dokumente\\Kontoauszüge"
logfile = "C:\\Users\\pabst\\Documents\\logfile.txt"
g_indent = ""


def browse_directory(indent, path, directory):
    file_indent = indent
    dir_indent = indent + "    "
    dir_path = path + '\\' + directory
    with os.scandir(dir_path) as dir_content:
        for dir_entry in dir_content:
            dir_info = dir_entry.stat()
            if dir_entry.is_file():
                name, ext = os.path.splitext(dir_entry.name)
                if ext.lower() == ".csv":
                    file.write(file_indent + "\t{0}, {1}\n".format(dir_entry.name, dir_info.st_size))
                    csv.reader()
            if dir_entry.is_dir():
                file.write(dir_indent + dir_entry.name + "\n")
                browse_directory(dir_indent, dir_path, dir_entry.name)


def browse_tree():
    with os.scandir(base_path) as dir_contents:
        for entry in dir_contents:
            if entry.is_dir():
                file.write(entry.name + "\n")
                browse_directory(g_indent, base_path, entry.name)


def browse_path():
    dir_content = Path(base_path)
    for entry in dir_content.iterdir():
        print(entry)


file = open(logfile, "w", encoding='utf-8')
browse_tree()
file.close()
