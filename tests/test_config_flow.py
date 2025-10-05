"""Tests for the Fear and Greed config flow."""

from __future__ import annotations

import pytest

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from custom_components.fear_and_greed.const import CONF_UPDATE_INTERVAL, DOMAIN


@pytest.mark.asyncio
async def test_user_flow_single_instance(hass: HomeAssistant) -> None:
    """The user flow should only allow a single instance."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == config_entries.FlowResultType.FORM

    result = await hass.config_entries.flow.async_configure(result["flow_id"], user_input={})
    assert result["type"] == config_entries.FlowResultType.CREATE_ENTRY
    assert result["title"] == "Fear & Greed Index"

    # Trying to create another entry should abort.
    second_flow = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert second_flow["type"] == config_entries.FlowResultType.ABORT
    assert second_flow["reason"] == "already_configured"


@pytest.mark.asyncio
async def test_options_flow(hass: HomeAssistant, mock_config_entry) -> None:
    """Ensure the options flow stores data correctly."""
    mock_config_entry.add_to_hass(hass)
    result = await hass.config_entries.options.async_init(mock_config_entry.entry_id)
    assert result["type"] == config_entries.FlowResultType.FORM

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={CONF_UPDATE_INTERVAL: 1800},
    )

    assert result["type"] == config_entries.FlowResultType.CREATE_ENTRY
    assert result["data"] == {CONF_UPDATE_INTERVAL: 1800}
