"""Tests for diagnostics output."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant.core import HomeAssistant

from custom_components.fear_and_greed import async_setup_entry
from custom_components.fear_and_greed.api import FearAndGreedIndex
from custom_components.fear_and_greed.diagnostics import async_get_config_entry_diagnostics


@pytest.mark.asyncio
async def test_diagnostics_returns_index(hass: HomeAssistant, mock_config_entry) -> None:
    """Diagnostics should include the current index."""
    index = FearAndGreedIndex(
        value=70,
        classification="Extreme Greed",
        previous_value=60,
        value_change=10,
        value_change_percent=16.67,
        last_updated=datetime(2024, 1, 1, 12, 0, 0),
    )

    mock_config_entry.add_to_hass(hass)
    with patch(
        "custom_components.fear_and_greed.api.FearAndGreedApiClient.async_get_index",
        AsyncMock(return_value=index),
    ):
        assert await async_setup_entry(hass, mock_config_entry)

    diagnostics = await async_get_config_entry_diagnostics(hass, mock_config_entry)
    assert diagnostics["index"]["value"] == 70
    assert diagnostics["index"]["classification"] == "Extreme Greed"
    assert diagnostics["index"]["value_change_percent"] == 16.67
