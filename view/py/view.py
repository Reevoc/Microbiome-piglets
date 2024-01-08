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

        print_tree(qzv_files_tree)
        choice = input(
            f"Enter the path to the qzv file you want to view (or 'exit' to quit): "
        )

        if choice.lower() == "exit":
            break

        file_path = os.path.join(base_path, choice)
        if os.path.exists(file_path):
            subprocess.run(["qiime", "tools", "view", file_path])
        else:
            print(f"{Fore.RED}Invalid path. Please enter a valid path.{Fore.RESET}")


if __name__ == "__main__":
    view_qzv_interactively()
