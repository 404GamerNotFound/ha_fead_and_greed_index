"""Client for retrieving data from the Alternative.me Fear and Greed API."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

import aiohttp

from .const import (
    ATTR_CHANGE,
    ATTR_CHANGE_PERCENT,
    ATTR_PREVIOUS_VALUE,
    JSON_TIMESTAMP,
    JSON_VALUE,
    JSON_VALUE_CLASSIFICATION,
)


class FearAndGreedApiClientError(Exception):
    """Raised when the API client encounters an error."""


@dataclass
class FearAndGreedIndex:
    """Represents the index returned by the API."""

    value: int
    classification: str
    previous_value: int | None
    value_change: int | None
    value_change_percent: float | None
    last_updated: datetime

    @property
    def as_sensor_attributes(self) -> Dict[str, Any]:
        """Return attributes for Home Assistant sensors."""
        attributes: Dict[str, Any] = {
            ATTR_PREVIOUS_VALUE: self.previous_value,
            ATTR_CHANGE: self.value_change,
            ATTR_CHANGE_PERCENT: self.value_change_percent,
        }
        return {key: value for key, value in attributes.items() if value is not None}


class FearAndGreedApiClient:
    """Fear and Greed API client."""

    def __init__(self, endpoint: str) -> None:
        self._endpoint = endpoint
        self._session: aiohttp.ClientSession | None = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def async_get_index(self) -> FearAndGreedIndex:
        """Retrieve the latest index data from the API."""
        session = await self._ensure_session()
        try:
            async with session.get(self._endpoint, params={"limit": 2}) as response:
                if response.status != 200:
                    raise FearAndGreedApiClientError(
                        f"Unexpected status {response.status} from Fear and Greed API"
                    )
                payload = await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            raise FearAndGreedApiClientError("Error communicating with Fear and Greed API") from err

        data = payload.get("data")
        if not data:
            raise FearAndGreedApiClientError("Fear and Greed API returned no data")

        latest = data[0]
        previous = data[1] if len(data) > 1 else None

        value = int(latest[JSON_VALUE])
        previous_value = int(previous[JSON_VALUE]) if previous else None
        value_change = value - previous_value if previous_value is not None else None
        value_change_percent = (
            (value_change / previous_value) * 100 if previous_value and value_change is not None else None
        )

        return FearAndGreedIndex(
            value=value,
            classification=latest.get(JSON_VALUE_CLASSIFICATION, "unknown"),
            previous_value=previous_value,
            value_change=value_change,
            value_change_percent=round(value_change_percent, 2) if value_change_percent is not None else None,
            last_updated=datetime.fromtimestamp(int(latest[JSON_TIMESTAMP])),
        )

    async def async_close(self) -> None:
        """Close the underlying session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> "FearAndGreedApiClient":
        await self._ensure_session()
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.async_close()
