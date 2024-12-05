from typing import Any

from cachetools import TTLCache

from mtmai.forge.sdk.cache.base import CACHE_EXPIRE_TIME, MAX_CACHE_ITEM, BaseCache


class LocalCache(BaseCache):
    def __init__(self) -> None:
        self.cache: TTLCache = TTLCache(
            maxsize=MAX_CACHE_ITEM, ttl=CACHE_EXPIRE_TIME.total_seconds()
        )

    async def get(self, key: str) -> Any:
        if key not in self.cache:
            return None
        value = self.cache[key]
        await self.set(key, value)
        return value

    async def set(self, key: str, value: Any) -> None:
        self.cache[key] = value
