# uscodekit/shared/file.py

import shutil
import os


def copy_file_to_dir(file_path: str, dest_dir: str) -> bool:
    """
    Copies a file to a specified directory.

    :param file_path: The path of the file to copy.
    :param dest_dir: The destination directory.
    :raises FileNotFoundError: If the file or directory does not exist.
    :raises ValueError: If the input is not a file.
    """
    try:
        # Check if the source file exists
        if not os.path.isfile(file_path):
            raise ValueError(f"The specified path is not a file: {file_path}")

        # Check if the destination directory exists
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # Copy the file to the destination directory
        shutil.copy(file_path, dest_dir)
        return True
    except Exception as e:
        return False


def rename_file(old_name: str, new_name: str) -> bool:
    """
    Renames a file using shutil.move.

    :param old_name: The current file path and name.
    :param new_name: The new file path and name.
    :raises FileNotFoundError: If the file to rename does not exist.
    """
    try:
        # Check if the file exists
        if not os.path.isfile(old_name):
            raise FileNotFoundError(f"The file '{old_name}' does not exist.")

        # Perform the rename operation
        shutil.move(old_name, new_name)
        return True
    except Exception as e:
        return False
