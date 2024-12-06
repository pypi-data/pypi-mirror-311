# uscodekit/shared/jsonfile.py

import json
from typing import List, Dict, Union, Any

from cryptography.fernet import Fernet

from uscodekit.configs import Config


def decrypt(file_path: str, key: Any = None) -> Dict:
    if key is None:
        with open(Config.encryption_key_fp, "rb") as key_file:
            key = key_file.read()

    cipher_suite = Fernet(key)

    with open(file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = cipher_suite.decrypt(encrypted_data)
    json_data = json.loads(decrypted_data.decode("utf-8"))

    return json_data


def encrypt(file_path: str, data: Dict, key: Any = None) -> None:
    if key is None:
        with open(Config.encryption_key_fp, "rb") as key_file:
            key = key_file.read()

    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(json.dumps(data).encode("utf-8"))

    with open(file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)


def read_data(file_path: str) -> Union[List[Dict], Dict, None]:
    try:
        with open(file_path, "r") as f:
            data = f.read()
            return json.loads(data)
    except FileNotFoundError as e:
        print(f"read_data: {e}")
        return None


def write_data(file_path: str, data: Union[List[Dict], Dict]) -> bool:
    try:
        with open(file_path, "w") as f:
            json.dump(data, f)
            return True
    except FileNotFoundError as e:
        print(f"write_data: {e}")
        return False
