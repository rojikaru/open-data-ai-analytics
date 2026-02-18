import polars as pl
from os import path, walk


GUESSING_ROOT = 'data/raw/'


def recursive_file_search(root_dir: str, extension: str = '.csv') -> list[str]:
    """
    Recursively search for files with a specific extension in a given directory.

    Parameters:
    root_dir (str): The root directory to start the search from.
    extension (str): The file extension to look for (default is '.csv').

    Returns:
    list[str]: A list of file paths that match the specified extension.
    """
    matching_files: list[str] = []

    for root, dirs, files in walk(root_dir):
        for file in files:
            if file.endswith(extension):
                matching_files.append(path.join(root, file))
        for dir in dirs:
            matching_files.extend(
                recursive_file_search(path.join(root, dir), extension)
)

    return matching_files


def load_data(
        guessing_root: str = GUESSING_ROOT,
        ignore_errors: bool = True,
        separator: str = ';',
        quote_char: str = '"',
) -> pl.DataFrame | None:
    """
    Load data from a CSV file in guessing_root into a Polars DataFrame.

    :param guessing_root (str): Where to start to look for a CSV using `os.walk()`
    :param ignore_errors (bool): Whether to ignore errors during CSV parsing (default is True).
    :param separator (str): The character used to separate fields in the CSV file (default is ';').
    :param quote_char (str): The character used to quote fields in the CSV file (default is '"').

    :returns: The loaded data as a Polars DataFrame, or None if loading fails.
    :rtype: pl.DataFrame | None
    """

    # Guess the file path based on the current working directory
    current_dir = path.dirname(path.abspath(__file__))
    guessing_root_abs = path.abspath(
        path.join(current_dir, '..', guessing_root)
    )

    # Find all CSV files in the guessing root directory
    csv_files = recursive_file_search(guessing_root_abs, extension='.csv')

    if not csv_files:
        print("No CSV files found in the guessing root directory.")
        return None

    # Load the first CSV file found
    file_path = csv_files[0]
    print(f"Loading data from: {file_path}")

    return pl.read_csv(
        file_path,
        ignore_errors=ignore_errors,
        try_parse_dates=True,
        truncate_ragged_lines=True,
        low_memory=False,
        separator=separator,
        quote_char=quote_char,
    )
