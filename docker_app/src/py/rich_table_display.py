import pandas as pd
from rich.console import Console
from rich.table import Table

def display_csv_summary_with_rich(file_path, max_rows=10):
    """
    Reads a CSV file and displays a summary table using Rich.

    Parameters:
    file_path (str): Path to the CSV file.
    max_rows (int): Maximum number of rows to display (default is 10).

    Returns:
    None
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)

        # Create a Rich console
        console = Console()

        # Create a Rich table
        table = Table(show_header=True, header_style="bold magenta")

        # Add columns to the table
        for column in df.columns:
            table.add_column(column)

        # Add rows to the table (up to max_rows)
        for _, row in df.head(max_rows).iterrows():
            table.add_row(*[str(item) for item in row])

        # Print the table
        console.print(table)

    except Exception as e:
        print(f"Error occurred: {e}")
