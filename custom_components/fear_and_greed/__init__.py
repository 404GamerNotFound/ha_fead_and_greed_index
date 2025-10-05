"""The Fear and Greed Index integration."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import FearAndGreedApiClient, FearAndGreedApiClientError
from .const import (
    API_ENDPOINT,
    CONF_UPDATE_INTERVAL,
    COORDINATOR_NAME,
    DOMAIN,
    PLATFORMS,
    SERVICE_REFRESH,
    UPDATE_INTERVAL,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA: ConfigType = {}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Fear and Greed from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    if not entry.options:
        hass.config_entries.async_update_entry(entry, options={CONF_UPDATE_INTERVAL: UPDATE_INTERVAL})

    update_interval = timedelta(seconds=entry.options.get(CONF_UPDATE_INTERVAL, UPDATE_INTERVAL))

    client = FearAndGreedApiClient(API_ENDPOINT)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=COORDINATOR_NAME,
        update_method=client.async_get_index,
        update_interval=update_interval,
    )

    try:
        await coordinator.async_config_entry_first_refresh()
    except FearAndGreedApiClientError as err:
        raise ConfigEntryNotReady(f"Error while setting up Fear and Greed integration: {err}") from err

    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "client": client,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def async_handle_refresh(call: ServiceCall) -> None:
        """Handle manual refresh service call."""
        await coordinator.async_request_refresh()

    if not hass.services.has_service(DOMAIN, SERVICE_REFRESH):
        hass.services.async_register(DOMAIN, SERVICE_REFRESH, async_handle_refresh)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        data = hass.data[DOMAIN].pop(entry.entry_id)
        await data["client"].async_close()
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_REFRESH)

    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Handle migration of config entry versions."""
    if config_entry.version == 1:
        _LOGGER.debug("Migrating Fear and Greed config entry from version 1 to 2")
        hass.config_entries.async_update_entry(
            config_entry,
            version=2,
            options={CONF_UPDATE_INTERVAL: UPDATE_INTERVAL},
        )
    return True
