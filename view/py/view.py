import os
import subprocess
from colorama import init, Fore
from utilities import find_qzv_files


def display_menu(qzv_files):
    print("\nAvailable .qzv files:")
    for i, qzv_file in enumerate(qzv_files):
        print(f"{Fore.CYAN}{i}.{Fore.RESET} {qzv_file}")
    print()


def view_qzv_interactively(
    base_path="/home/piermarco/Documents/Thesis/docker_app/data",
):
    while True:
        # Find and show the available qzv files
        qzv_files_path = find_qzv_files(base_path)

        # Check if there are any qzv files
        if not qzv_files_path:
            print(f"{Fore.RED}No .qzv files found in the specified path.{Fore.RESET}")
            return

        # Ask the user to choose a qzv file
        display_menu(qzv_files_path)
        choice = input(
            f"Enter the number of the qzv file you want to view (or '{Fore.RED}exit{Fore.RESET}' to quit): "
        )

        if choice.lower() == "exit":
            break

        try:
            choice = int(choice)
            if 0 <= choice < len(qzv_files_path):
                qzv_file = qzv_files_path[choice]
                subprocess.run(["qiime", "tools", "view", qzv_file])
            else:
                print(
                    f"{Fore.RED}Invalid choice. Please enter a valid number.{Fore.RESET}"
                )
        except ValueError:
            print(
                f"{Fore.RED}Invalid input. Please enter a number or '{Fore.RED}q{Fore.RESET}' to quit.{Fore.RESET}"
            )


if __name__ == "__main__":
    view_qzv_interactively()
