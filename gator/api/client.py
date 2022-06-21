"""Web client for the Gator API."""
from typing import Any
from urllib.parse import urljoin

from gator.api.helpers import add_url_params


class GatorClient:
    """Web client for the Gator API."""
    def __init__(self, base_url: str, encoding: str = 'utf8') -> None:
        """Initialize the client.

        Args:
            base_url: The base URL of the Gator API service.
            encoding: The encoding to use for the requests.
        """
        self._base_url = base_url
        self._encoding = encoding

    def _compose_url(self, path: str, **params: Any) -> str:
        """Compose a URL for the given path.

        Args:
            path: The path to compose the URL for. This path is relative to the
                base URL.
            **params: The parameters to include in the URL.

        Returns:
            The composed URL.

        >>> client = GatorClient('http://localhost:5000')
        >>> client._compose_url('/api/v1/users', name='John', age=42)
        'http://localhost:5000/api/v1/users?name=John&age=42'
        """
        url = urljoin(self._base_url, path)
        return add_url_params(url, **params)