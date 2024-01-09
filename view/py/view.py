from utilities import find_qzv_files, print_tree, get_file_from_tree
from colorama import Fore
import subprocess
import os


def view_qzv_interactively(base_path="/home/piermarco/Documents/Thesis/data"):
    while True:
        qzv_files_tree = find_qzv_files(base_path)

        if not qzv_files_tree:
            print(f"{Fore.RED}No .qzv files found in the specified path.{Fore.RESET}")
            return

        tree = print_tree(qzv_files_tree)
        choice = input("Enter the number of the file you want to view: ")
        if choice == "exit":
            return
        if not choice.isdigit():
            print(f"{Fore.RED}Invalid input. Please enter a number.{Fore.RESET}")
            continue
        choice = int(choice)
        if choice not in tree:
            print(f"{Fore.RED}Invalid input. Please enter a valid number.{Fore.RESET}")
            continue
        choice = tree[choice][0]
        print(choice)
        file_path = os.path.join(base_path, choice)
        if os.path.exists(file_path):
            subprocess.run(["qiime", "tools", "view", file_path])
        else:
            print(f"{Fore.RED}Invalid path. Please enter a valid path.{Fore.RESET}")


if __name__ == "__main__":
    view_qzv_interactively()
