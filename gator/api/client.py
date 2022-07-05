"""Web client for the Gator API."""
import json
from typing import Any, Optional
from urllib.parse import urljoin

import certifi
import urllib3

from gator.api.helpers import add_url_params
from gator.schemas.timetable import CourseSchema


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
        self._connection_pool = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )

    # Private methods
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

    def _request(self, method: str, path: str, **params: Any) \
            -> tuple[Any, int]:
        """Make a request to the Gator API.

        Args:
            method: The HTTP method to use for the request.
            path: The path to the resource to request. This path is relative to
                the base URL.
            params: The parameters to include in the request given as a
                dictionary of key-value pairs. If None, no parameters are
                included in the request.

        Returns:
            A tuple containing the JSON response and the HTTP status code.
        """
        url = self._compose_url(path, **params)
        response = self._connection_pool.urlopen(method.upper(), url)

        body = json.loads(response.data.decode(self._encoding))
        return body, response.status

    def _construct_params(self, **kwargs: Any) -> dict:
        """Construct a dictionary of parameters from the given keyword
        arguments. If a keyword argument is None, it is not included in the
        resultant parameter dictionary.

        Args:
            **kwargs: The keyword arguments to include in the parameters.

        Returns:
            A dictionary of parameters.
        """
        params = {}
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        return params

    # API methods
    def get_courses(self, page_size: Optional[int] = None,
                    last_id: Optional[str] = None) -> dict:
        """GET /courses.

        Args:
            page_size: The number of items to return per page.
            last_id: The id of the last item returned.
        """
        params = self._construct_params(
            page_size=page_size,
            last_id=last_id
        )

        body, _ = self._request('GET', '/courses', **params)
        return CourseSchema().load(
            body.get('courses', []),
            many=True
        )
