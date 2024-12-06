# src/phone.py

import re
from typing import Optional, List, Dict
from uscodekit.services.geo import GeoService


US_PHONE_PATTERN = re.compile(
    r"""
    (?:(?:\+1)[\s.-]?)?                 # Optional country code (+1)
    (?:\((\d{3})\)|(\d{3}))[\s.-]?      # Area code with or without parentheses (must be matched correctly)
    (\d{3})[\s.-]?                      # First 3 digits (required)
    (\d{4})                             # Last 4 digits (required)
    """,
    re.VERBOSE,
)


def is_valid_phone(phone: str) -> bool:
    """
    Validates if the provided phone number matches the U.S. phone number format.

    This function checks if the given phone number string conforms to the standard
    U.S. phone number format, which typically includes a 3-digit area code, followed
    by a 3-digit central office code, and a 4-digit station number. The phone number
    may also include country code (+1) and can be formatted with or without dashes,
    spaces, or parentheses.

    Args:
        phone (str): The phone number string to validate.

    Returns:
        bool: True if the phone number matches the U.S. phone number format, False otherwise.
    """
    return bool(US_PHONE_PATTERN.fullmatch(phone))


def extract_phone_number(text: str) -> Optional[str]:
    """
    Formats a valid U.S. phone number to the standard format: (123) 456-7890.

    Args:
        text (str): The text string to find phone from. It should contain a valid U.S. phone number.

    Returns:
        str: The phone number formatted in the standard U.S. format (123) 456-7890.

    Raises:
        ValueError: If the input phone number is not a valid U.S. phone number.

    Example:
        >>> extract_phone_number("1234567890")
        '(123) 456-7890'
    """
    try:
        matched_phone = US_PHONE_PATTERN.findall(text)[0]
        phone = "".join(matched_phone)
        cleaned = cleaned_phone(phone)
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    except Exception:
        return None


def extract_phone_numbers(text: str) -> List[str]:
    """
    Extracts all U.S. phone numbers from a given text.

    This function searches the input text for patterns that match the format of U.S. phone numbers
    and returns a list of formatted phone numbers. The expected format for the phone numbers is
    (XXX) XXX-XXXX, where X is a digit from 0 to 9.

    Args:
        text (str): The input text from which to extract phone numbers.

    Returns:
        list of str: A list of strings, each representing a U.S. phone number in the format (XXX) XXX-XXXX.

    Example:
        >>> extract_phone_numbers("Contact us at (123) 456-7890 or (987) 654-3210.")
        ['(123) 456-7890', '(987) 654-3210']
    """
    results = []
    try:
        matched_phones = US_PHONE_PATTERN.findall(text)
        for matched_phone in matched_phones:
            ph = extract_phone_number("".join(matched_phone))
            if ph:
                results.append(ph)
    except ValueError:
        pass
    finally:
        return results


def get_area_code(phone: str) -> str:
    """
    Extracts the area code from a given US phone number.

    Args:
        phone (str): The phone number in string format.

    Returns:
        str: The extracted area code.

    Raises:
        AttributeError: If the phone number does not match the expected pattern.
    """
    try:
        return US_PHONE_PATTERN.match(phone).group(1)
    except AttributeError:
        raise AttributeError("Invalid U.S. phone number")


def cleaned_phone(phone: str) -> str:
    """
    Cleans up a U.S. phone number by removing all non-numeric characters.

    This function takes a phone number as input, removes all characters that are not digits,
    and returns a cleaned-up version of the phone number. The function ensures that the
    returned phone number is a valid 10-digit U.S. phone number.

    Args:
        phone (str): The phone number to be cleaned. This can include non-numeric characters
                     such as spaces, dashes, parentheses, etc.

    Returns:
        str: A cleaned 10-digit U.S. phone number.

    Raises:
        ValueError: If the cleaned phone number does not have exactly 10 digits, or if it has
                    11 digits but does not start with the country code '1'.
    """
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 10:
        return digits
    elif len(digits) == 11 and digits.startswith("1"):
        return digits[1:]  # Remove leading country code
    else:
        raise ValueError("Invalid U.S. phone number for cleaning")


def prettify(phone_str: str) -> Optional[str]:
    """
    Formats a US phone number string into a more readable format.

    This function removes any non-numeric characters from the input string and
    formats it into the standard US phone number format (XXX) XXX-XXXX. It
    supports phone numbers with 10 digits or 11 digits (if the leading digit is '1').

    Args:
        phone_str (str): The phone number string to be formatted.

    Returns:
        str | None: The formatted phone number string if the input is valid,
                    otherwise None.
    """
    # Remove any non-numeric characters
    digits = re.sub(r"\D", "", phone_str)

    # Check if it has exactly 10 or 11 digits (11 if includes leading '1' for US)
    if len(digits) == 10:
        formatted_number = f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == "1":
        formatted_number = f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        raise ValueError("Invalid U.S. phone number for prettifying")

    return formatted_number


def phone_number_insight(phone: str) -> Dict[str, Optional[str]]:
    """
    Provides detailed information about a given phone number.

    This function takes a phone number as input, extracts its area code,
    and retrieves related information such as city, state, zip code,
    location coordinates, and timezone from a database service.

    Args:
        phone (str): The phone number to be analyzed.

    Returns:
        dict: A dictionary containing the following keys:
            - phone (str): The prettified phone number.
            - areaCode (str): The area code of the phone number.
            - city (str): The city associated with the area code.
            - state (str): The state associated with the area code.
            - stateISO (str): The ISO code of the state.
            - zipCode (str): The zip code associated with the area code.
            - location (dict): A dictionary with 'latitude' and 'longitude' of the area.
            - timezone (dict): A dictionary with 'name' and 'offset' of the timezone.
    """
    cp = cleaned_phone(phone)
    pp = prettify(cp)
    area_code = get_area_code(pp)
    npa_db = GeoService()
    pinfo = npa_db.get_phone_info(area_code)
    return {
        "phone": pp,
        "areaCode": area_code,
        "city": pinfo.get("city", ""),
        "state": pinfo.get("state", ""),
        "stateISO": pinfo.get("stateISO", ""),
        "zipCode": pinfo.get("zipCode", ""),
        "location": pinfo.get("location", {"latitude": "", "longitude": ""}),
        "timezone": pinfo.get("timezone", {"name": "", "offset": ""}),
    }
