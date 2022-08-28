"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator, UpdateFailed)

import asyncio
import collections
import socket
import json

from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)

class MonitorConnection(DataUpdateCoordinator):
    """Dummy hub for Hello World example."""

    manufacturer = "bgfxc4"
    online = True
    _power_state = False
    firmware_version = "N/A"
    model = "N/A"
    name = "N/A"

    cpu_list = {}
    average_cpu_load = 0

    isFirstDataLoad = True
    sensorConfigEntry: ConfigEntry = None

    def __init__(self, hass: HomeAssistant, host: str, port: int, password: str) -> None:
        """Init dummy hub."""
        self._host = host
        self._hass = hass
        self._port = port
        self._password = password
        self._id = (host+str(port)).lower()

        self.server_address = (host, port)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30)
        )

    async def _async_update_data(self):
        await self.get_state_from_device()

    async def get_state_from_device(self) -> bool:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        res = False
        try:
            sock.connect(self.server_address)
            message = {
                "token": "state",
                "password": self._password
            }
            sock.sendall(bytes(json.dumps(message)+"\n\n", encoding="utf-8"))
            res = json.loads(sock.recv(1048))
            self._power_state = True
            if (collections.Counter(self.cpu_list.keys()) != collections.Counter(res["data"]["state"]["cpu"]["cores"].keys())) and self.sensorConfigEntry != None:
                await self._hass.config_entries.async_forward_entry_unload(
                    self.sensorConfigEntry, "sensor"
                )
                self.cpu_list = res["data"]["state"]["cpu"]["cores"]
                await self._hass.config_entries.async_forward_entry_setup(
                    self.sensorConfigEntry, "sensor"
                )
            else:
                self.cpu_list = res["data"]["state"]["cpu"]["cores"]

            self.average_cpu_load = res["data"]["state"]["cpu"]["average"]
            self.firmware_version = f'{res["data"]["info"]["kernel_version"]} {res["data"]["info"]["os_version"]}'
            self.name = f'{res["data"]["info"]["system_name"]}'
            self.model = f'{res["data"]["info"]["system_name"]}'
        except Exception as e:
            print("Exception:" + e)
            self._power_state = False
            return False
        finally:
            sock.close()
            return res

    @property
    def connection_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    @property
    def power_state(self) -> bool:
        return self._power_state

    @property
    def cpu_load(self) -> bool:
        return self._cpu_load
