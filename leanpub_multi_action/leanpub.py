"""Leanpub API Client and Helpers.

API Docs: https://leanpub.com/help/api
API URL: https://leanpub.com/
"""

from typing import Optional, Tuple

import requests


class Leanpub(requests.Session):
    """Leanpub API Client object.

    Based upon the requests.session object, so all underlying requests methods available.

    Requires a Leanpub API Key to be instantiated.
    """

    def __init__(self, leanpub_api_key: str, **kwargs: dict) -> None:
        """Instantiate a Leanpub client.

        Args:
            leanpub_api_key (str): A valid Leanpub API Key
        """
        super().__init__(**kwargs)
        self.leanpub_api_key = leanpub_api_key
        self.leanpub_url = "https://leanpub.com/"

    def preview(self, book_slug: str) -> Tuple[Optional[requests.Response], Optional[requests.RequestException]]:
        """Request a Preview be built of the book_slug provided.

        Args:
            book_slug (str): book_slug to generate a Preview of
        """
        url = f"{self.leanpub_url}{book_slug}/preview.json"
        payload = {"api_key": self.leanpub_api_key}
        try:
            resp = self.post(url=url, json=payload)
            resp.raise_for_status()
        except requests.RequestException as exception:
            return None, exception

        return resp, None
