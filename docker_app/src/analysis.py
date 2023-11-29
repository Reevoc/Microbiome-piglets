import subprocess
from colorama import Fore, Style


def print_message(message, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{style}{color}{message}{Style.RESET_ALL}")


def print_explanation(message, color=Fore.YELLOW, style=Style.BRIGHT):
    print_message(message, color, style)


sh_normalization = "/home/microbiome/src/with_normalization.sh"
sh_metrics = "/home/microbiome/src/metricsAB.sh"

print_explanation(
    "This script will execute normalization on the data and then run the metrics script. The data is organized in folders for better pipeline understanding. Inside each folder, the first number represents the pipeline order, the second number represents the taxa analyzed (1=asv, 2=genus, 3=species), and the rest describes the taxa level. You can also find .qza or .qzv .biom files used for the analysis.\n"
)

print_explanation(
    "Normalization can be done using 3 taxa types: \n 1) asv --> normalize on asv \n 2) genus --> normalize on genus \n 3) species --> normalize on species \n "
)

print_explanation(
    "We recommend using 'all' to ensure the script works correctly. Some metrics, such as Alpha and Beta, cannot be calculated otherwise.\n"
)

taxa_type = input("Enter taxa type (asv, genus, species): ")

try:
    if (
        (taxa_type != "asv")
        and (taxa_type != "genus")
        and (taxa_type != "species")
        and (taxa_type != "all")
    ):
        raise ValueError
except ValueError:
    print_message("Error: taxa type not valid. Please enter a valid taxa type.")
    exit()

imputation_type = "nrm"

if taxa_type != "asv":
    print_explanation(
        "selected genus or species so you can also select the imputation method \n 1)st--> impouatnon normalizied \n 2)nrm --> imputed normalizied \n 3)lgn --> lgn normalizied"
    )

    imputation_type = input("Enter imputation type (st, nrm, lng): ")

    try:
        if (
            (imputation_type != "st")
            and (imputation_type != "nrm")
            and (imputation_type != "lgn")
        ):
            raise ValueError
    except ValueError:
        print_message(
            "Error: imputation type not valid. Please enter a valid imputation type."
        )
        exit()

print_explanation(
    "Normalization can be done using 2 metrics: \n 1) gmpr --> launch gmpr normalization \n 2) clr --> launch clr normalization \n"
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
    subprocess.run(
        ["bash", sh_normalization, taxa_type, normalization_type, imputation_type]
    )
except subprocess.CalledProcessError:
    print_message("Error during normalization. Taxa type not equal to 'all'.")

try:
    subprocess.run(["bash", sh_metrics, taxa_type, normalization_type])
except subprocess.CalledProcessError:
    print_message("Error during metrics. Taxa type not equal to 'all'.")

print_explanation("Do you want to see the results? (yes, no)")

see_results = input("Enter yes or no: ")

try:
    if (see_results != "yes") and (see_results != "no"):
        raise ValueError
except ValueError:
    print_message("Error: see results not valid. Please enter a valid see results.")
    exit()

print_explanation("Do you want to eliminate the intermediate files? (yes, no)")

eliminate_files = input("Enter yes or no: ")

try:
    if (eliminate_files != "yes") and (eliminate_files != "no"):
        raise ValueError
except ValueError:
    print_message(
        "Error: eliminate files not valid. Please enter a valid eliminate files."
    )

if eliminate_files == "yes":
    print_explanation(
        "Do you want to eliminate all the analysis done, or just the alpha and beta metrics? (all, onlyAB)"
    )

    eliminate = input("Enter all or onlyAB: ")

    try:
        if (eliminate != "all") and (eliminate != "onlyAB"):
            raise ValueError
    except ValueError:
        print_message(
            "Error: eliminate all not valid. Please enter a valid eliminate all."
        )
        exit()
