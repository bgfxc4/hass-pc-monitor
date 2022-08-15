"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator, UpdateFailed)

import socket
import json

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


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (host, port)

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
        res = False
        try:
            self.sock.connect(self.server_address)
            message = {
                "token": "auth",
                "password": self._password
            }
            self.sock.sendall(bytes(json.dumps(message), encoding="utf-8"))
            res = json.loads(self.sock.recv(1048))
        except Exception as e:
            return False
        finally:
            self.sock.close()
            return res

    @property
    def power_state(self) -> bool:
        return self._power_state

    @property
    def cpu_load(self) -> bool:
        return self._cpu_load
