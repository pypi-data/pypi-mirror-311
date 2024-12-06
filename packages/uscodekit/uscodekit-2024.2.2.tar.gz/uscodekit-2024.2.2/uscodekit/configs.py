from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "uscodekit"
DATA_DIR = SRC_DIR / "data"
CREDS_DIR = SRC_DIR / "creds"


class DirConfig:
    root_dir = PROJECT_ROOT
    src_dir = SRC_DIR
    data_dir = DATA_DIR


class GeoConfig:
    encrypted_database_filename = "geo.gz"
    root = DATA_DIR / "geo"
    encrypted_database_fp = root / "geo.gz"
    decompressed_data_fp = root / "decompressed.geo.bin"
    decompressed_json_fp = root / "decompressed.geo.json"


class NAICS2022Config:
    edition = "2022"
    root = DATA_DIR / "naics/2022"
    encrypted_database_filename = "naics.bin"
    encrypted_database_fp = root / "naics.bin"
    search_data_fp = root / "naics.json"


class Config:
    dir = DirConfig
    geo = GeoConfig
    root = CREDS_DIR
    encryption_key_name = "encryption.key"
    encryption_key_fp = CREDS_DIR / "encryption.key"
    file_missing_message = "'''\nPlease contact the owner of this package for the \ngeo database and encryption key. To get original results.\nhttps://github.com/rk4bir\n'''"
