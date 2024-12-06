import os
from typing import Dict

from uscodekit.configs import Config
from uscodekit.configs import NAICS2022Config
from uscodekit.configs import GeoConfig
from uscodekit.shared.file import copy_file_to_dir, rename_file


def setup_file_stats(verbose: bool = True) -> Dict:
    """
    Checks the existence of various configuration files and returns their status.

    This function verifies the presence of the encryption key, geo database,
    and NAICS database files. It prints the status of each file (either "OK"
    if the file exists or "MISSING" if it does not) and returns a dictionary
    indicating the presence of each file.

    Returns:
        Dict: A dictionary with the following keys:
            - "encryption_key" (bool): True if the encryption key file exists, False otherwise.
            - "geo_database" (bool): True if the geo database file exists, False otherwise.
            - "naics_database" (bool): True if the NAICS database file exists, False otherwise.
    """
    info = {"encryption_key": False, "geo_database": False, "naics_database": False}
    if verbose:
        print("Encryption key...", end="")
    if os.path.isfile(Config.encryption_key_fp):
        if verbose:
            print("OK")
        info["encryption_key"] = True
    else:
        if verbose:
            print("MISSING")

    if verbose:
        print("Geo database...", end="")
    if os.path.isfile(GeoConfig.encrypted_database_fp):
        if verbose:
            print("OK")
        info["geo_database"] = True
    else:
        if verbose:
            print("MISSING")

    if verbose:
        print("NAICS database...", end="")
    if os.path.isfile(NAICS2022Config.encrypted_database_fp):
        if verbose:
            print("OK")
        info["naics_database"] = True
    else:
        if verbose:
            print("MISSING")

    return info


def setup_geo_database(file_path: str) -> bool:
    """
    Sets up the geo database by copying the provided .gz file to the specified directory.

    Args:
        file_path (str): The path to the .gz file that needs to be used for setting up the geo database.

    Returns:
        bool: True if the geo database setup is completed successfully, False otherwise.

    Raises:
        ValueError: If the provided file does not have a .gz extension.

    Notes:
        - If the geo database is already set up, the function will print a message and return True.
        - If an error occurs during the file copy process, the function will print the error message and return False.
    """
    stats: Dict = setup_file_stats(verbose=False)
    file_name = file_path.split(os.sep)[-1]
    # validate file name
    ext = GeoConfig.encrypted_database_filename.split(".")[-1]
    if not file_name.endswith(f".{ext}"):
        raise ValueError(f"Invalid file format. Please provide the .{{ext}} file.")

    # check if the file exists
    if stats["geo_database"]:
        print("Geo database setup is already completed.")
        return True

    try:
        copy_file_to_dir(file_path, GeoConfig.root)
        # rename the file to the expected name
        rename_file(old_name=file_path, new_name=GeoConfig.encrypted_database_fp)
        print("Geo database setup is completed.")
        return True
    except Exception as e:
        print(f"Error setting up geo database: {e}")
        return False


def setup_naics_database(file_path: str) -> bool:
    """
    Sets up the NAICS database by copying the provided .bin file to the specified directory.

    Args:
        file_path (str): The path to the .bin file that needs to be used for setting up the NAICS database.

    Returns:
        bool: True if the NAICS database setup is completed successfully, False otherwise.

    Raises:
        ValueError: If the provided file does not have a .bin extension.

    Notes:
        - If the NAICS database is already set up, the function will print a message and return True.
        - If an error occurs during the file copy process, the function will print the error message and return False.
    """
    stats: Dict = setup_file_stats(verbose=False)
    file_name = file_path.split(os.sep)[-1]

    ext = NAICS2022Config.encrypted_database_filename.split(".")[-1]
    # validate file name
    if not file_name.endswith(f".{ext}"):
        raise ValueError(f"Invalid file format. Please provide the .{{ext}} file.")

    # check if the file exists
    if stats["naics_database"]:
        print("NAICS database setup is already completed.")
        return True

    try:
        copy_file_to_dir(file_path, NAICS2022Config.root)
        # rename the file to the expected name
        rename_file(old_name=file_path, new_name=NAICS2022Config.encrypted_database_fp)
        print("NAICS database setup is completed.")
        return True
    except Exception as e:
        print(f"Error setting up NAICS database: {e}")
        return False


def setup_encryption_key(file_path: str) -> bool:
    """
    Sets up the encryption key by copying the provided .key file to the specified directory.

    Args:
        file_path (str): The path to the .key file that needs to be used for setting up the encryption key.

    Returns:
        bool: True if the encryption key setup is completed successfully, False otherwise.

    Raises:
        ValueError: If the provided file does not have a .key extension.

    Notes:
        - If the encryption key is already set up, the function will print a message and return True.
        - If an error occurs during the file copy process, the function will print the error message and return False.
    """
    stats: Dict = setup_file_stats(verbose=False)
    file_name = file_path.split(os.sep)[-1]
    ext = Config.encryption_key_name.split(".")[-1]

    # validate file name
    if not file_name.endswith(f".{ext}"):
        raise ValueError(f"Invalid file format. Please provide the .{{ext}} file.")

    # check if the file exists
    if stats["encryption_key"]:
        print("Encryption key setup is already completed.")
        return True

    try:
        copy_file_to_dir(file_path, Config.root)
        # rename the file to the expected name
        rename_file(old_name=file_path, new_name=Config.encryption_key_fp)
        print("Encryption key setup is completed.")
        return True
    except Exception as e:
        print(f"Error setting up encryption key: {e}")
        return False


def setup_all() -> None:
    """
    Sets up all configuration files required for the package.

    This function prompts the user to provide the paths for the encryption key, geo database,
    and NAICS database files, and then sets up these files by copying them to the specified directories.
    It prints the status of each file setup operation.
    """
    encryption_key_path = input("Enter the path to the encryption key file: ")
    geo_database_path = input("Enter the path to the geo database file: ")
    naics_database_path = input("Enter the path to the NAICS database file: ")

    setup_encryption_key(encryption_key_path)
    setup_geo_database(geo_database_path)
    setup_naics_database(naics_database_path)
