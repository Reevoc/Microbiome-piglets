import csv
import sys
import utility


def read_args():
    """Read args given to python script"""
    taxa_type = sys.argv[1]
    normalization = sys.argv[2]
    quantile_num = sys.argv[3]
    taxa_number = {"asv": "1", "genus": "2", "species": "3"}.get(taxa_type, "1")
    return taxa_number, taxa_type, normalization, quantile_num


def create_path_csv(taxa_number, taxa_type, normalization="gmpr"):
    """Create path to csv file"""
    path = f"/home/microbiome/data/10.{taxa_number}_{taxa_type}_{normalization}_table_norm/{taxa_type}_{normalization}_summary.csv"
    return path


def take_information_csv(path_csv, quantile_num):
    """Take information from csv file"""
    frequency = utility.read_csv(path_csv, quantile_num)
    sample_frequency = frequency[0][0]
    feature_frequency = frequency[0][1]
    return sample_frequency, feature_frequency


def main():
    """Main function"""
    taxa_number, taxa_type, normalization, quantile = read_args()
    path_csv = create_path_csv(taxa_number, taxa_type, normalization)
    sample_frequency, feature_frequency = take_information_csv(path_csv, quantile)
    print(sample_frequency, feature_frequency)


if __name__ == "__main__":
    main()
