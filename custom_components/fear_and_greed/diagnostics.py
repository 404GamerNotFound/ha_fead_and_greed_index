"""Diagnostics support for the Fear and Greed integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, object]:
    """Return diagnostics for a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    index = coordinator.data

    if not index:
        return {"index": None}

    return {
        "index": {
            "value": index.value,
            "classification": index.classification,
            "previous_value": index.previous_value,
            "value_change": index.value_change,
            "value_change_percent": index.value_change_percent,
            "last_updated": index.last_updated.isoformat(),
        }
    }
