from __future__ import annotations
from homeassistant.components import bluetooth
from homeassistant.components.bluetooth import BluetoothScanningMode
from .const import DOMAIN
import logging

LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Set up LEDDMX from a config entry."""

    def _discovered_device(service_info, change):
        """Handle discovery of a new LEDDMX device."""
        LOGGER.debug("Doscovered Device with name %s - ",service_info.name)
        if service_info.name and service_info.name.startswith("LEDDMX-03"):
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN,
                    context={"source": "bluetooth"},
                    data=service_info,
                )
            )

    # Register for Bluetooth discovery events (works with ESPHome proxy too)
    entry.async_on_unload(
        bluetooth.async_register_callback(
            hass,
            _discovered_device,
            None,
            bluetooth.BluetoothScanningMode.ACTIVE,
        )
    )
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, ["light"])
    )
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    return True
