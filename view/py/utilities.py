import os
import subprocess
import re


def extract_number(s):
    if "." in s:
        s = s.replace(".", "")
        return int(s)
    else:
        return int(s + "0")


def find_qzv_files(base_path):
    qzv_files = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".qzv"):
                qzv_files.append(os.path.join(root, file))

    ordered_qzv_files = sorted(
        qzv_files, key=lambda x: extract_number((x.split("/")[-2]).split("_")[0])
    )

    return ordered_qzv_files


def eliminate_all_analysis_done(path="/home/microbiome/data", values=["10", "11"]):
    for root, dirs, files in os.walk(path):
        for current_dir in dirs:
            for value in values:
                if re.search(value, current_dir):
                    dir_path = os.path.join(root, current_dir)
                    subprocess.run(["rm", "-rf", dir_path])
                    print(f"Deleted {dir_path}")
