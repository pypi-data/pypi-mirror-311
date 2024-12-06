# PBFUS1/metadata.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import yaml
import importlib.resources

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

def load_metadata():
    """
    Loads metadata from a CSV file specified in the configuration.

    Returns:
        pd.DataFrame: DataFrame containing the metadata information from 'resume.csv'.

    Raises:
        FileNotFoundError: If the specified CSV file is not found.
        pd.errors.EmptyDataError: If the CSV file is empty.
    """
    config = load_config()
    csv_path = os.path.join(config["download_dir"], "resume.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}. Please ensure the dataset is downloaded.")
    
    try:
        metadata = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("The CSV file is empty. Please ensure it contains data.")
    return metadata


def load_studies_metadata():
    """
    Loads metadata from a CSV file specified in the configuration.

    Returns:
        pd.DataFrame: DataFrame containing the metadata information from 'resume.csv'.

    Raises:
        FileNotFoundError: If the specified CSV file is not found.
        pd.errors.EmptyDataError: If the CSV file is empty.
    """
    config = load_config()
    csv_path = os.path.join(config["download_dir"], "metadata.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}. Please ensure the dataset is downloaded.")
    
    try:
        metadata = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("The CSV file is empty. Please ensure it contains data.")
    return metadata

def count_elements_per_class():
    """
    Counts the number of elements for each class value in the metadata.

    Returns:
        dict: A dictionary where keys are class values and values are the counts of elements in each class.
    """
    metadata = load_metadata()
    class_counts = metadata.groupby("value").size()
    class_names = metadata.groupby("value")["class"].first()
    
    for value, count in class_counts.items():
        class_name = class_names[value]
        print(f"Class '{class_name}' (Value: {value}): {count} elements")
    
    class_counts = metadata.groupby("value").size().to_dict()
    return class_counts

def print_class_names_with_values():
    """
    Prints the available classes along with their corresponding values in the dataset.
    """
    metadata = load_metadata()
    unique_classes = metadata[['class', 'value']].drop_duplicates()
    print("Classes available with their values:")
    for _, row in unique_classes.iterrows():
        print(f"- Class: {row['class']}, Value: {row['value']}")

def get_images_by_class_value(class_value):
    """
    Retrieves the filenames of images associated with a specified class value.

    Args:
        class_value (int): The value of the class to filter images by.

    Returns:
        pd.Series: A Series containing filenames of images that match the specified class value.

    Raises:
        ValueError: If the specified class value does not exist in the metadata.
    """
    metadata = load_metadata()
    
    if class_value not in metadata["value"].values:
        raise ValueError(f"Class value '{class_value}' does not exist in the dataset.")
    
    filtered_metadata = metadata[metadata["value"] == class_value]
    return filtered_metadata["file_name"]

def plot_random_images(num_images_per_class, fig_size=(15, 5)):
    """
    Displays a specified number of random images for each class in the metadata dataset, sorted by class value.
    
    Args:
        num_images_per_class (int): The number of random images to display for each class.
        fig_size (tuple): The size of the figure (width, height) for each row.
    
    Raises:
        ValueError: If there are not enough images for a specified class.
        FileNotFoundError: If any specified image file in the metadata is not found in the directory.
    """
    config = load_config()
    download_dir = config["download_dir"]
    metadata = load_metadata()
    
    unique_classes = sorted(metadata['value'].unique())
    
    fig, axes = plt.subplots(len(unique_classes), num_images_per_class + 1, 
                             figsize=(fig_size[0], fig_size[1] * len(unique_classes)), 
                             gridspec_kw={'width_ratios': [0.5] + [1] * num_images_per_class})
    fig.suptitle(f"{num_images_per_class} Random Images per Class", fontsize=16)

    for i, class_value in enumerate(unique_classes):
        class_metadata = metadata[metadata["value"] == class_value]
        
        if len(class_metadata) < num_images_per_class:
            print(f"Warning: Not enough images in class '{class_value}'. Showing all available images.")
            samples = class_metadata
        else:
            samples = class_metadata.sample(n=num_images_per_class)

        class_name = class_metadata["class"].iloc[0].replace("standard plane", "S.P.")
        axes[i, 0].text(0.5, 0.5, f"{class_name}\n(Value: {class_value})", ha='center', va='center', 
                        fontsize=12, rotation=90)
        axes[i, 0].axis("off")
        
        for j, (_, row) in enumerate(samples.iterrows()):
            folder = row["studie"]
            image_name = row["file_name"]

            image_path = os.path.join(download_dir, folder, image_name)
            
            if os.path.exists(image_path):
                image = cv2.imread(image_path)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                axes[i, j + 1].imshow(image_rgb)
                axes[i, j + 1].axis("off")
            else:
                print(f"Warning: Image '{image_name}' listed in metadata not found at '{image_path}'.")
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.9, hspace=0.1)
    plt.show()
