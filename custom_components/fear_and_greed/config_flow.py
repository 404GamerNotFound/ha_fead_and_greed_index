"""Config flow for the Fear and Greed integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_UPDATE_INTERVAL, DOMAIN, UPDATE_INTERVAL


class FearAndGreedConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Fear and Greed integration."""

    VERSION = 2

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Fear & Greed Index", data={})

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        return FearAndGreedOptionsFlowHandler(config_entry)


class FearAndGreedOptionsFlowHandler(config_entries.OptionsFlow):
    """Options flow for the integration."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        """Manage the options for the integration."""
        return await self.async_step_update()

    async def async_step_update(self, user_input: dict[str, Any] | None = None):
        if user_input is not None:
            return self.async_create_entry(title="Fear & Greed Options", data=user_input)

        return self.async_show_form(
            step_id="update",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(CONF_UPDATE_INTERVAL, UPDATE_INTERVAL),
                    ): vol.All(vol.Coerce(int), vol.Clamp(min=900, max=21600)),
                }
            ),
        )
