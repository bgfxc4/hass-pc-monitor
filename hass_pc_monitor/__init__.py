"""The Detailed Hello World Push integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .monitorConnection import MonitorConnection
from .const import DOMAIN

PLATFORMS: list[str] = ["binary_sensor", "sensor", "button"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = MonitorConnection(hass, entry.data["host"], entry.data["port"], entry.data["password"])
    await hass.data[DOMAIN][entry.entry_id].get_state_from_device()
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
