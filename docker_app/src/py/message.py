import os
from colorama import Fore, Style

def print_message(message, color=Fore.LIGHTBLUE_EX, style=Style.NORMAL):
    print(f"{style}{color}{message}{Style.RESET_ALL}")


def print_explanation(message, color=Fore.YELLOW, style=Style.BRIGHT):
    print_message(message, color, style)


