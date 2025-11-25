from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
import logging
from typing import Any, Dict, AsyncContextManager

import httpx

from .constants import BASE_URL, HEADERS


logger = logging.getLogger(__name__)


class BaseProxy(ABC):

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self._base_url: str = base_url.rstrip('/')
        self._timeout: float = timeout
        self.session_headers: Dict[str, str] = {}

    @asynccontextmanager
    async def client(self) -> AsyncContextManager[httpx.AsyncClient]:
        req_headers = self.get_default_headers()
        req_headers.update(self.session_headers)

        async with httpx.AsyncClient(
            base_url=self._base_url,
            headers=req_headers,
            timeout=self._timeout
        ) as client:
            yield client

    @abstractmethod
    def get_default_headers(self) -> Dict[str, str]:
        """
        Return the default headers for the proxy,
        which is class-level configuration
        """
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        """
        Path of API endpoint
        """
        pass

    @abstractmethod
    def build_http_params(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """
        Build HTTP parameters for the API request
        for GET request, would be for query string parameters
        for POST request, would be for request body parameters
        """
        pass

    async def fetch(self, *args: Any, **kwargs: Any) -> httpx.Response:
        params = self.build_http_params(*args, **kwargs)
        async with self.client() as client:
            return await client.get(self.path, params=params)


class NBAProxy(BaseProxy, ABC):
    """
    for nba.com series API requests

    implement the following methods for subclasses:
      - path: define the path of API endpoint
      - build_http_params: build HTTP parameters for the API request
      - fetch: only overwrite the docstring and arguments
    """

    def __init__(self, timeout: float = 30.0) -> None:
        super().__init__(BASE_URL, timeout)

    def get_default_headers(self) -> Dict[str, str]:
        return HEADERS
