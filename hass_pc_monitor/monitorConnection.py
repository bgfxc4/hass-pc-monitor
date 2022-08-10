"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator, UpdateFailed)

from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)

class MonitorConnection(DataUpdateCoordinator):
    """Dummy hub for Hello World example."""

    manufacturer = "bgfxc4"

    def __init__(self, hass: HomeAssistant, host: str, port: int, password: str) -> None:
        """Init dummy hub."""
        self._host = host
        self._hass = hass
        self._name = host
        self.name = host
        self._port = port
        self._password = password
        self._id = (host+str(port)).lower()
        self.online = True

        self._power_state = True
        self._cpu_load = 69

        self.firmware_version = "0.0.1"
        self.model = "PC Monitor"

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30)
        )

    async def _async_update_data(self):
        try:
            #print("API Call Device")
            pass
        except:
            raise UpdateFailed("Error Talking to Device API")

    @property
    def connection_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        await asyncio.sleep(1)
        return True


    @property
    def power_state(self) -> bool:
        return self._power_state

    @property
    def cpu_load(self) -> bool:
        return self._cpu_load
