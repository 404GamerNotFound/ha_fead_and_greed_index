"""Tests for the API client."""

from __future__ import annotations

import pytest

from custom_components.fear_and_greed.api import FearAndGreedApiClient, FearAndGreedApiClientError


@pytest.mark.asyncio
async def test_api_handles_non_200(aioclient_mock) -> None:
    """The client should raise when the status code is not 200."""
    aioclient_mock.get("https://api.alternative.me/fng/", status=500)

    client = FearAndGreedApiClient("https://api.alternative.me/fng/")

    with pytest.raises(FearAndGreedApiClientError):
        await client.async_get_index()


@pytest.mark.asyncio
async def test_api_parses_payload(aioclient_mock, sample_api_payload) -> None:
    """The client should parse the API payload correctly."""
    aioclient_mock.get("https://api.alternative.me/fng/", json=sample_api_payload)

    client = FearAndGreedApiClient("https://api.alternative.me/fng/")
    index = await client.async_get_index()

    assert index.value == 56
    assert index.previous_value == 48
    assert index.value_change == 8
    assert index.value_change_percent == pytest.approx(16.67, rel=1e-2)
    await client.async_close()
