import re
from typing import Optional, List, Dict, Any
from uscodekit.services.geo import GeoService


def extract_zip_code(text: str) -> Optional[str]:
    """
    Extracts a US ZIP code from the given text.

    This function uses a regular expression to search for a US ZIP code in the
    provided text. It supports both the 5-digit format and the ZIP+4 format.

    Args:
        text (str): The text from which to extract the ZIP code.

    Returns:
        Optional[str]: The extracted ZIP code if found, otherwise None.
    """
    # Regular expression for US ZIP codes: 5-digit or ZIP+4 format
    zip_code_pattern = r"\b\d{5}(?:-\d{4})?\b"

    match = re.search(zip_code_pattern, text)
    if match:
        return match.group()  # Return the matched ZIP code
    else:
        return None


def extract_all_zip_codes(text: str) -> List[str]:
    """
    Extracts all US ZIP codes from the given text.

    This function uses a regular expression to find all US ZIP codes in the
    provided text. It supports both the 5-digit format and the ZIP+4 format.

    Args:
        text (str): The text from which to extract the ZIP codes.

    Returns:
        List[str]: A list of extracted ZIP codes (empty if none found).
    """
    # Regular expression for US ZIP codes: 5-digit or ZIP+4 format
    zip_code_pattern = r"\b\d{5}(?:-\d{4})?\b"

    return re.findall(zip_code_pattern, text)


def zip_code_insight(zip_code: str) -> Dict[str, Any]:
    """
    Provides detailed information about a given ZIP code.

    This function retrieves information related to the provided ZIP code,
    including area code, city, state, state ISO code, location (latitude and longitude),
    and timezone details.

    Args:
        zip_code (str): The ZIP code for which information is to be retrieved.

    Returns:
        Dict[str, Any]: A dictionary containing the following keys:
            - zipCode (str): The provided ZIP code.
            - areaCode (str): The area code associated with the ZIP code.
            - city (str): The city associated with the ZIP code.
            - state (str): The state associated with the ZIP code.
            - stateISO (str): The ISO code of the state.
            - location (dict): A dictionary containing latitude and longitude.
                - latitude (str): The latitude of the location.
                - longitude (str): The longitude of the location.
            - timezone (dict): A dictionary containing timezone information.
                - name (str): The name of the timezone.
                - offset (str): The offset of the timezone from UTC.
    """
    npa_db = GeoService()
    pinfo = npa_db.get_zip_code_info(zip_code)
    return {
        "zipCode": zip_code,
        "areaCode": pinfo.get("npa", ""),
        "city": pinfo.get("city", ""),
        "state": pinfo.get("state", ""),
        "stateISO": pinfo.get("stateISO", ""),
        "location": pinfo.get("location", {"latitude": "", "longitude": ""}),
        "timezone": pinfo.get("timezone", {"name": "", "offset": ""}),
    }
