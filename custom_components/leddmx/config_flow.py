from __future__ import annotations
from homeassistant import config_entries
from homeassistant.components import bluetooth
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from .const import DOMAIN

class LEDDMXConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_bluetooth(self, discovery_info):
        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title=discovery_info.name or "LEDDMX Light",
            data={
                "address": discovery_info.address,
                "name": discovery_info.name,
            },
        )
    async def async_step_user(self, user_input=None):
        """Manual setup (optional)."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=vol.Schema({vol.Optional("address"): str}))
        
        # Use provided address or default name
        return self.async_create_entry(
            title=user_input.get("address", "LEDDMX Light"),
            data={"address": user_input.get("address"), "name": "Manual LEDDMX"},
        )
