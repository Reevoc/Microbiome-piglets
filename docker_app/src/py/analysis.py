import subprocess
from colorama import Fore, Style


def print_message(message, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{message}{Style.RESET_ALL}")


def print_explanation(message, color=Fore.YELLOW, style=Style.BRIGHT):
    print_message(message, color, style)


sh_normalization = "/home/microbiome/docker_app/src/sh/normalization.sh"
sh_metrics = "/home/microbiome/docker_app/src/sh/metricsAB.sh"

print_explanation(
    "This script will execute normalization on the data and then run the metrics script. The data is organized in folders for better pipeline understanding. Inside each folder, the first number represents the pipeline order, the second number represents the taxa analyzed (1=asv, 2=genus, 3=species), and the rest describes the taxa level. You can also find .qza or .qzv .biom files used for the analysis.\n"
)

print_explanation(
    "Normalization can be done using 3 taxa types: \n 1) asv --> normalize on asv \n 2) genus --> normalize on genus \n 3) species --> normalize on species\n "
)

taxa_type = input("Enter taxa type (asv, genus, species): ")

try:
    if (taxa_type != "asv") and (taxa_type != "genus") and (taxa_type != "species"):
        raise ValueError
except ValueError:
    print_message("\nError: taxa type not valid. Please enter a valid taxa type.\n")
    exit()

print_explanation(
    "\n Normalization can be done using 2 metrics: \n 1) gmpr --> launch gmpr normalization \n 2) clr --> launch clr normalization \n"
)

print_explanation(
    "We recommend using 'gmpr' to ensure the script works correctly. CLR normalization may have issues with negative values.\n"
)

normalization_type = input("Enter normalization type (gmpr, clr): ")

try:
    if (normalization_type != "gmpr") and (normalization_type != "clr"):
        raise ValueError
except ValueError:
    print_message(
        "Error: normalization type not valid. Please enter a valid normalization type."
    )
    exit()

print("\n")

try:
    subprocess.run(["bash", sh_normalization, taxa_type, normalization_type])
except subprocess.CalledProcessError:
    print_message("\nError during normalization input wrong\n")

try:
    subprocess.run(["bash", sh_metrics, taxa_type, normalization_type])
except subprocess.CalledProcessError:
    print_message("\nError during metrics input wrong\n")
