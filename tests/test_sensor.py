"""Tests for the Fear and Greed sensors."""

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant.const import ATTR_ATTRIBUTION, PERCENTAGE
from homeassistant.core import HomeAssistant

from custom_components.fear_and_greed import async_setup_entry
from custom_components.fear_and_greed.api import FearAndGreedIndex
from custom_components.fear_and_greed.const import (
    ATTR_CHANGE,
    ATTR_CHANGE_PERCENT,
    ATTR_CLASSIFICATION,
    ATTR_PREVIOUS_VALUE,
    DOMAIN,
)


@pytest.mark.asyncio
async def test_sensors_create_entities(hass: HomeAssistant, mock_config_entry, sample_api_payload) -> None:
    """Ensure that the sensors are created with correct state and attributes."""
    index = FearAndGreedIndex(
        value=int(sample_api_payload["data"][0]["value"]),
        classification=sample_api_payload["data"][0]["value_classification"],
        previous_value=int(sample_api_payload["data"][1]["value"]),
        value_change=8,
        value_change_percent=round(((56 - 48) / 48) * 100, 2),
        last_updated=datetime.fromtimestamp(int(sample_api_payload["data"][0]["timestamp"])),
    )

    mock_config_entry.add_to_hass(hass)

    with patch(
        "custom_components.fear_and_greed.api.FearAndGreedApiClient.async_get_index",
        AsyncMock(return_value=index),
    ):
        assert await async_setup_entry(hass, mock_config_entry)

    await hass.async_block_till_done()

    index_entity_id = "sensor.fear_and_greed_index"
    sentiment_entity_id = "sensor.fear_and_greed_sentiment"

    state = hass.states.get(index_entity_id)
    assert state is not None
    assert state.state == "56"
    assert state.attributes["unit_of_measurement"] == PERCENTAGE
    assert state.attributes[ATTR_PREVIOUS_VALUE] == 48
    assert state.attributes[ATTR_CHANGE] == 8
    assert state.attributes[ATTR_CHANGE_PERCENT] == pytest.approx(16.67, rel=1e-2)
    assert state.attributes[ATTR_CLASSIFICATION] == "Greed"
    assert state.attributes[ATTR_ATTRIBUTION] == "Data provided by Alternative.me"

    sentiment_state = hass.states.get(sentiment_entity_id)
    assert sentiment_state is not None
    assert sentiment_state.state == "Greed"
    assert sentiment_state.attributes["icon"] == "mdi:emoticon-excited-outline"


@pytest.mark.asyncio
async def test_manual_refresh_service(hass: HomeAssistant, mock_config_entry) -> None:
    """The manual refresh service should request a new update."""
    index_first = FearAndGreedIndex(
        value=50,
        classification="Neutral",
        previous_value=45,
        value_change=5,
        value_change_percent=11.11,
        last_updated=datetime.utcnow(),
    )

    index_second = FearAndGreedIndex(
        value=65,
        classification="Greed",
        previous_value=50,
        value_change=15,
        value_change_percent=30.0,
        last_updated=datetime.utcnow(),
    )

    client_patch = "custom_components.fear_and_greed.api.FearAndGreedApiClient.async_get_index"
    mock = AsyncMock(side_effect=[index_first, index_second])

    mock_config_entry.add_to_hass(hass)
    with patch(client_patch, mock):
        assert await async_setup_entry(hass, mock_config_entry)

    await hass.async_block_till_done()

    state = hass.states.get("sensor.fear_and_greed_index")
    assert state.state == "50"

    await hass.services.async_call(DOMAIN, "refresh", blocking=True)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.fear_and_greed_index")
    assert state.state == "65"
    assert mock.call_count == 2
