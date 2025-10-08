import asyncio
import logging
from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_RGB_COLOR, ColorMode, LightEntity
)
from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.components import bluetooth
from bleak import BleakClient
from .const import DOMAIN, CHAR_UUID

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([LEDDMXLight(entry.data)], True)

class LEDDMXLight(LightEntity):
    def __init__(self, config):
        self._name = config.get(CONF_NAME)
        self._address = config.get(CONF_ADDRESS)
        self._is_on = False
        self._color = (255, 255, 255)
        self._brightness = 255

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._is_on

    @property
    def supported_color_modes(self):
        return {ColorMode.RGB}

    @property
    def color_mode(self):
        return ColorMode.RGB

    @property
    def rgb_color(self):
        return self._color

    async def _write_ble(self, data: bytes):
        _LOGGER.debug("Sending BLE data to %s: %s", self._address, data.hex())
        device = bluetooth.async_ble_device_from_address(self.hass, self._address, connectable=True)
        if not device:
            _LOGGER.warning("Device not found: %s", self._address)
            return
        async with BleakClient(device) as client:
            await client.write_gatt_char(CHAR_UUID, data, response=False)

    async def async_turn_on(self, **kwargs):
        self._is_on = True
        # rgb = kwargs.get(ATTR_RGB_COLOR, self._color)
        # self._color = rgb
        # brightness = kwargs.get(ATTR_BRIGHTNESS, self._brightness)
        # self._brightness = brightness

        # r, g, b = [int(c * brightness / 255) for c in rgb]
        # # Normal RGB packet
        # packets = [
        #     bytes.fromhex(f"7B0503{r:02X}{g:02X}{b:02X}FFBF"),
        #     bytes.fromhex(f"7EFF0503{r:02X}{g:02X}{b:02X}FFEF"),
        # ]

        # # Example effects: fade, flash, jump (common LEDDMX codes)
        # effect = kwargs.get("effect")
        # if effect == "fade":
        #     packets.append(bytes.fromhex("7B0504FFFFFFFFBF"))
        # elif effect == "flash":
        #     packets.append(bytes.fromhex("7B0503FFFFFFFFBF"))
        # elif effect == "jump":
        #     packets.append(bytes.fromhex("7B0505FFFFFFFFBF"))

        # await self._write_any(packets)
        await self._write_ble(bytes.fromhex("7B040401FFFFFFFFBF"))
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._is_on = False
        packets = [
            bytes.fromhex("7B040400FFFFFFFFBF"),
            bytes.fromhex("7EFF0400FFFFFFFFEF"),
        ]
        await self._write_any(packets)
        self.async_write_ha_state()

    async def _write_any(self, packets):
        for pkt in packets:
            try:
                _LOGGER.debug("Trying packet %s", pkt.hex())
                await self._write_ble(pkt)
                return
            except Exception as e:
                _LOGGER.debug("Packet failed %s", e)
                continue
        _LOGGER.warning("All packet variants failed for %s", self._address)