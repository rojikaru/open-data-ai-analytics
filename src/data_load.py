import polars as pl
import requests

import shutil
from os import listdir, mkdir, path

from src.constants import RAW_DATA_ROOT


def download_file(url: str, target_folder: str) -> str:
    """
    Download a file from a given URL and save it to a specified path.

    :param url (str): The URL of the file to download.
    :param target_folder (str): The local folder where the downloaded file should be saved.

    :return (str): The path to the saved file.
    """

    file_name = url.split('/')[-1]
    file_path = path.join(target_folder, file_name)
    if path.exists(file_path):
        return file_path
    
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"Failed to download file from URL: {url}")

    with open(file_path, 'wb') as f:
        f.write(response.content)

    return file_path


def handle_maybe_zip_or_csv(file_path: str) -> str:
    """
    Handle a file that may be either a ZIP archive or a CSV file. 
    If it's a ZIP archive, extract it and return the path to the contained CSV file.

    :param file_path (str): The path to the file to handle.

    :return (str): The path to the CSV file, whether it 
    was directly provided or extracted from a ZIP archive.
    """

    if not file_path.endswith('.zip'):  
        return file_path
    
    folder_name = path.splitext(path.basename(file_path))[0]
    folder_path = path.join(
        path.dirname(file_path),
        folder_name
    )

    if not path.exists(folder_path):
        shutil.unpack_archive(file_path, folder_path)

    # Assuming the ZIP contains a single CSV file, find it
    csv_files = [file for file in listdir(folder_path) if file.endswith('.csv')]
    if not csv_files:
        raise ValueError(f"No CSV file found in the ZIP archive: {file_path}")

    return path.join(folder_path, csv_files[0])


def load_data(
        url: str,
        clear_cache: bool = False,
        ignore_errors: bool = True,
        separator: str = ';',
        quote_char: str = '"',
) -> pl.DataFrame | None:
    """
    Load data from a CSV file in guessing_root into a Polars DataFrame.

    :param url (str): The URL or path to the CSV or ZIP file to load.
    :param ignore_errors (bool): Whether to ignore errors during CSV parsing (default is True).
    :param separator (str): The character used to separate fields in the CSV file (default is ';').
    :param quote_char (str): The character used to quote fields in the CSV file (default is '"').

    :returns: The loaded data as a Polars DataFrame, or None if loading fails.
    :rtype: pl.DataFrame | None
    """

    current_dir = path.dirname(path.abspath(__file__))
    raw_data_root_abs = path.abspath(
        path.join(current_dir, '..', RAW_DATA_ROOT)
    )

    if clear_cache:
        shutil.rmtree(raw_data_root_abs)

    # Ensure the raw data root directory exists
    if not path.exists(raw_data_root_abs):
        mkdir(raw_data_root_abs)

    downloaded_file_path = download_file(url, raw_data_root_abs)
    file_path = handle_maybe_zip_or_csv(downloaded_file_path)
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
