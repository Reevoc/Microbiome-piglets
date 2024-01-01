import csv
import sys


def read_args():
    """Read args given to python script"""
    taxa_type = sys.argv[1]
    normalization = sys.argv[2]
    quantile = sys.argv[3]
    taxa_number = {"asv": "1", "genus": "2", "species": "3"}.get(taxa_type, "1")
    return taxa_number, taxa_type, normalization, quantile


def create_path_csv(taxa_number, taxa_type, normalization):
    """Create path to csv file"""
    path = f"/home/microbiome/data/10.{taxa_number}_{taxa_type}_{normalization}_table_norm/{taxa_type}_{normalization}_summary.csv"
    return path


def open_csv(path_csv):
    """Open csv file"""
    with open(path_csv, "r", newline="") as file:
        reader = csv.reader(file)
        data = list(reader)
    return data


def take_information_csv(data, quantile):
    """Take information from csv file"""
    index_mapping = {
        "min": 1,
        "first": 2,
        "median": 3,
        "second": 4,
        "max": 5,
        "medium": 6,
    }
    index = index_mapping.get(quantile, 1)  # Default to 'min' if quantile is not found
    sample_frequency = data[index][1]
    feature_frequency = data[index][2]
    return sample_frequency, feature_frequency


def main():
    """Main function"""
    taxa_number, taxa_type, normalization, quantile = read_args()
    path_csv = create_path_csv(taxa_number, taxa_type, normalization)
    data = open_csv(path_csv)
    sample_frequency, feature_frequency = take_information_csv(data, quantile)
    print(sample_frequency, feature_frequency)


if __name__ == "__main__":
    main()
