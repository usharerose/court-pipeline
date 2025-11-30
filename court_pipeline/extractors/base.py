import asyncio
import httpx
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence

from ..s3.base import S3MixIn


logger = logging.getLogger(__name__)


class ExtractorProtocol(Protocol):

    async def fetch(self, *args: Any, **kwargs: Any) -> httpx.Response: ...

    async def store_object(self, data: bytes, content_type: str) -> None: ...


class BaseExtractorMixIn:

    async def extract(self: ExtractorProtocol, *args: Any, **kwargs: Any) -> None:
        response = await self.fetch(*args, **kwargs)
        content_type = "application/json"
        content = response.content
        await self.store_object(content, content_type)
