import os
import requests
import zipfile
from tqdm import tqdm
import yaml
import importlib.resources
import pandas as pd

from .metadata import load_metadata

def load_config():
    """
    Loads the configuration settings from the 'config.yaml' file included in the package.

    The configuration file should contain settings such as:
    - dataset_url: URL of the dataset to download
    - download_dir: Directory to download and extract the dataset files

    This function ensures that the 'config.yaml' file is loaded correctly from the package
    and is accessible even when the package is installed in a different location.

    Returns:
        dict: A dictionary containing configuration parameters from 'config.yaml'.

    Raises:
        FileNotFoundError: If the 'config.yaml' file does not exist in the package directory.
        yaml.YAMLError: If there is an error in the YAML file format.
    """
    try:
        # Use importlib.resources to locate the file in the installed package
        with importlib.resources.open_text("PBFUS1", "config.yaml") as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(
            "The 'config.yaml' file was not found. Please ensure it exists in the package directory."
        )
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing 'config.yaml': {e}")
    return config

def download_dataset():
    """
    Downloads and extracts a dataset from a specified URL.
    
    This function reads the dataset URL and download directory from the configuration
    loaded by `load_config()`. It then downloads the dataset as a ZIP file, saves it
    in the specified directory, and extracts its contents.
    
    The structure of 'config.yaml' should be:
    - dataset_url: URL to download the dataset (e.g., "https://example.com/dataset.zip")
    - download_dir: Directory where the dataset will be saved and extracted
    
    Raises:
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
        zipfile.BadZipFile: If the downloaded file is not a valid ZIP file.
    """
    config = load_config()
    dataset_url = config.get("dataset_url")
    download_dir = config.get("download_dir")

    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, "dataset.zip")

    try:
        response = requests.get(dataset_url, stream=True)
        response.raise_for_status()  # Check for HTTP errors
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to download dataset: {e}")

    try:
        with open(file_path, "wb") as f:
            for chunk in tqdm(response.iter_content(chunk_size=1024), desc="Downloading dataset"):
                if chunk:
                    f.write(chunk)
    except IOError as e:
        raise IOError(f"Failed to write dataset to disk: {e}")

    try:
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(download_dir)
    except zipfile.BadZipFile:
        raise zipfile.BadZipFile(f"The downloaded file '{file_path}' is not a valid ZIP file.")
    
    print(f"Dataset downloaded and extracted to {download_dir}")

def load_images_info():
    """
    Loads metadata from an Excel or CSV file and adds a column with full image paths.
    
    The function reads the download directory from the configuration using `load_config()`
    and expects the metadata file to contain `studie` and `file_name` columns.
    
    Returns:
        pandas.DataFrame: A DataFrame containing the metadata with an added 'image_path' column.
    
    Raises:
        Exception: If loading metadata or configuration fails.
    """
    config = load_config()
    download_dir = config.get("download_dir")
    
    try:
        metadata = load_metadata()  # Load metadata as a DataFrame
    except Exception as e:
        raise Exception(f"Failed to load metadata: {e}")
    
    # Add the 'image_path' column to the DataFrame
    metadata["image"] = metadata.apply(
        lambda row: os.path.join(download_dir, row["studie"], row["file_name"]), axis=1
    )
    
    return metadata
