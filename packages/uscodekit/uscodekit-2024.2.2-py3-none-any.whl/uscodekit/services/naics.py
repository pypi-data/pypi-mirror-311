import os
from functools import lru_cache
from typing import List, Optional, Dict

from uscodekit.configs import NAICS2022Config, Config
from uscodekit.shared.jsonfile import decrypt


class NAICS2022Service:

    def __init__(self):
        if os.path.isfile(Config.encryption_key_fp) and os.path.isfile(
            NAICS2022Config.encrypted_database_fp
        ):
            self.data = self.search_database
        else:
            print(Config.file_missing_message)
            self.data = []

    @property
    @lru_cache(maxsize=1)
    def search_database(self) -> List[Dict]:
        """
        Property that returns a cached list of dictionaries representing the search database.

        This method reads data from the file path specified in the NAICS2022Config.search_data_fp
        and caches the result to improve performance on subsequent accesses.

        Returns:
            list[dict]: A list of dictionaries containing the search database data.
        """

        if os.path.isfile(Config.encryption_key_fp) and os.path.isfile(
            NAICS2022Config.encrypted_database_fp
        ):
            return decrypt(NAICS2022Config.encrypted_database_fp)
        else:
            print(Config.file_missing_message)
            return []

    def get(self, code: str) -> Optional[Dict]:
        """
        Retrieve a dictionary from the search database that matches the given code.

        Args:
            code (str): The code to search for in the database.

        Returns:
            dict | None: The dictionary that matches the given code if found, otherwise None.
        """
        res = list(filter(lambda x: x["code"] == code, self.data))
        return res[0] if res else None

    def industry_name(self, code: str) -> Optional[str]:
        """
        Retrieve the industry name from the search database that matches the given code.

        Args:
            code (str): The code to search for in the database.

        Returns:
            dict | None: The dictionary that matches the given code if found, otherwise None.
        """
        try:
            return self.get(code)["title"]
        except Exception as e:
            return None

    def search(self, query: str, top_n: int = 10) -> List[Dict]:
        """
        Searches the database for matches on both 'code' and 'title' fields,
        prioritizing exact matches, prefix matches, and then partial matches.

        Parameters:
            query (str): The search query to match against both 'code' and 'title'.

        Returns:
            list: A sorted list of dictionaries matching the query, ranked by relevance.

        Example:
        >>> search('Public Finance') =>
        [
            {'code': '92113', 'title': 'Public Finance Activities'},
            {'code': '921130', 'title': 'Public Finance Activities'}
        ]
        """
        # Normalize the query
        query = query.strip().lower()

        # Define scoring criteria
        results = []

        for entry in self.data:
            code = entry["code"]
            title = entry["title"].lower()

            # Initialize relevance score
            relevance_score = 0

            # Check for exact matches in code or title (highest relevance)
            if query == code or query == title:
                relevance_score = 3
            # Check for prefix match in code (high relevance)
            elif code.startswith(query):
                relevance_score = 2
            # Check for partial match in title (medium relevance)
            elif query in title:
                relevance_score = 1

            # If there's a match, add to results with relevance score
            if relevance_score > 0:
                results.append((relevance_score, entry))

        # Sort results by relevance score in descending order
        results.sort(key=lambda x: x[0], reverse=True)

        # Return only the matched entries, without scores
        return [entry for _, entry in results[:top_n]]

    def industry_hierarchy(self, code: str) -> Optional[Dict]:
        """
        Generates a hierarchical representation of NAICS code data based on the given code,
        handling different lengths (2, 3, 4, 5, or 6 digits).

        Parameters:
            code (str): The NAICS code for which to generate the hierarchy.

        Returns:
            dict: A hierarchical dictionary with details up to the specified code length.
        """
        rec = self.get(code)
        if rec is None:
            return None

        # Initialize the hierarchy dictionary
        hierarchy = {
            "sector": None,
            "subsector": None,
            "industry_group": None,
            "naics_industry": None,
            "national_industry": None,
        }

        # Determine hierarchy based on the length of the code
        if len(code) >= 2:
            hierarchy["sector"] = self.get(code[:2])
        if len(code) >= 3:
            hierarchy["subsector"] = self.get(code[:3])
        if len(code) >= 4:
            hierarchy["industry_group"] = self.get(code[:4])
        if len(code) >= 5:
            hierarchy["naics_industry"] = self.get(code[:5])
        if len(code) == 6:
            hierarchy["national_industry"] = self.get(code)

        # Build the final record with available levels
        record = {
            "code": code,
            "title": rec.get("title"),
            "sector": hierarchy["sector"],
            "subsector": hierarchy["subsector"],
            "industry_group": hierarchy["industry_group"],
            "naics_industry": hierarchy["naics_industry"],
            "national_industry": hierarchy["national_industry"],
        }

        # Remove None entries for levels not included based on code length
        return {k: v for k, v in record.items() if v is not None}
