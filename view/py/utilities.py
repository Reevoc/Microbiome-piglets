import os
import subprocess
import re
from colorama import Fore, Style


def natural_sort_key(s, _nsre=re.compile("([0-9]+)")):
    return [
        int(text) if text.isdigit() else text.lower() for text in re.split(_nsre, s)
    ]


def find_qzv_files(base_path):
    qzv_files = {}
    for root, dirs, files in os.walk(base_path):
        dirs.sort(key=natural_sort_key)  # Sort directories numerically
        for file in files:
            if file.endswith(".qzv"):
                dir_key = root.replace(base_path, "").strip("/")
                if dir_key not in qzv_files:
                    qzv_files[dir_key] = []
                qzv_files[dir_key].append(file)
    return qzv_files


def print_tree(qzv_files):
    for dir_key, files in sorted(
        qzv_files.items(), key=lambda x: natural_sort_key(x[0])
    ):
        print(f"|{Style.BRIGHT}{Fore.GREEN}{dir_key}/{Style.RESET_ALL}")
        print("|")
        for file in sorted(files, key=natural_sort_key):
            print(f"|___________{Fore.LIGHTBLUE_EX}{file}{Style.RESET_ALL}")


def extract_number(s):
    if "." in s:
        s = s.replace(".", "")
        return int(s)
    else:
        return int(s + "0")


def get_file_from_tree(current_dict, keys):
    for key in keys:
        current_dict = current_dict.get(key, {})
        if not isinstance(current_dict, dict):
            return current_dict
    return None
