# src/utils.py

import os
import gzip
import shutil
import json
from functools import lru_cache
from typing import List, Dict

from cryptography.fernet import Fernet

from uscodekit.configs import Config, GeoConfig


@lru_cache(maxsize=1)
def get_cached_database() -> List[Dict]:
    try:
        if not os.path.isfile(GeoConfig.decompressed_json_fp):
            return False
        with open(GeoConfig.decompressed_json_fp, "rb") as f:
            data = f.read()
            return json.loads(data)
    except FileNotFoundError as e:
        print(f"get_cached_database: {e}")
        return []


def get_database() -> List[Dict]:
    try:
        print("Loading encrypted database...", end="")
        # retrieve encryption key
        with open(Config.encryption_key_fp, "rb") as key_file:
            key = key_file.read()

        cipher_suite = Fernet(key)

        # Check if the decompressed data file exists
        if not os.path.exists(GeoConfig.decompressed_data_fp):
            with gzip.open(GeoConfig.encrypted_database_fp, "rb") as f_in, open(
                GeoConfig.decompressed_data_fp, "wb"
            ) as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Load and decrypt the data
        with open(GeoConfig.decompressed_data_fp, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = cipher_suite.decrypt(encrypted_data)
        json_data = json.loads(decrypted_data.decode("utf-8"))

        print("OK")
        # Cache the data
        with open(GeoConfig.decompressed_json_fp, "w") as f:
            f.write(json.dumps(json_data))
        if isinstance(json_data, list):
            return json_data
        return []
    except FileNotFoundError as e:
        print("FAILED")
        print(Config.file_missing_message)
        return []


class GeoService:
    """
    A service class to interact with a database containing geographical information.

    Methods
    -------
    database : list
        Property that returns the cached database if available, otherwise fetches the database.
        If the database file is not found, it prints a message and returns an empty list.

    get_phone_info(area_code: str) -> dict
        Returns information related to a given area code from the database.
        If no information is found, returns an empty dictionary.

    get_zip_code_info(zip_code: str) -> dict
        Returns information related to a given zip code from the database.
        If no information is found, returns an empty dictionary.
    """

    @property
    def database(self) -> List[Dict]:
        if not os.path.isfile(GeoConfig.encrypted_database_fp):
            print(Config.file_missing_message)
            return []

        cached = get_cached_database()
        if cached:
            return cached
        return get_database()

    def get_phone_info(self, area_code: str) -> Dict:
        result = list(filter(lambda x: x["npa"] == area_code, self.database))
        return result[0] if result else {}

    def get_zip_code_info(self, zip_code: str) -> Dict:
        result = list(filter(lambda x: x["zipCode"] == zip_code, self.database))
        return result[0] if result else {}
