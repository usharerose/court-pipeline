"""
Test cases for BaseProxy
"""
import pytest

import httpx

from court_pipeline.proxy.base import BaseProxy


class MockProxy(BaseProxy):

    def get_default_headers(self) -> dict:
        return {"User-Agent": "test-proxy"}

    @property
    def path(self) -> str:
        return "/test/endpoint"

    def build_http_params(self, *args, **kwargs) -> dict:
        return {"param1": "value1"}


class TestBaseProxy:

    def test_initialization(self):
        proxy = MockProxy("https://api.test.com", timeout=30.0)

        assert proxy._base_url == "https://api.test.com"
        assert proxy._timeout == 30.0
        assert isinstance(proxy.session_headers, dict)

    def test_initialization_with_custom_timeout(self):
        proxy = MockProxy("https://api.test.com", timeout=60.0)
        assert proxy._timeout == 60.0

    def test_base_url_stripping(self):
        proxy = MockProxy("https://api.test.com/")
        assert proxy._base_url == "https://api.test.com"

        proxy2 = MockProxy("https://api.test.com")
        assert proxy2._base_url == "https://api.test.com"

    @pytest.mark.asyncio
    async def test_client_creation(self):
        proxy = MockProxy("https://api.test.com")

        async with proxy.client() as client:
            assert isinstance(client, httpx.AsyncClient)
            assert client.base_url == "https://api.test.com"
            assert client.headers["User-Agent"] == "test-proxy"

    @pytest.mark.asyncio
    async def test_client_with_session_headers(self):
        proxy = MockProxy("https://api.test.com")
        proxy.session_headers["Authorization"] = "Bearer token"

        async with proxy.client() as client:
            assert client.headers["User-Agent"] == "test-proxy"
            assert client.headers["Authorization"] == "Bearer token"

    def test_abstract_methods(self):
        with pytest.raises(TypeError):
            BaseProxy("https://api.test.com")
