"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator, UpdateFailed)

import collections
import socket
import json

from .const import DOMAIN
_LOGGER = logging.getLogger(__name__)

class MonitorConnection(DataUpdateCoordinator):
    """Dummy hub for Hello World example."""

    manufacturer = "bgfxc4"
    _power_state = False
    firmware_version = "N/A"
    model = "N/A"
    name = "N/A"

    cpu_list = {}
    average_cpu_load = 0

    memory = {
        "memory": {"total": 0, "used": 0},
        "swap": {"total": 0, "used": 0}
    }

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
            sock.settimeout(1)
            sock.connect(self.server_address)
            message = {
                "token": "state",
                "password": self._password
            }
            sock.sendall(bytes(json.dumps(message)+"\n\n", encoding="utf-8"))
            res = json.loads(sock.recv(1048))
            self._power_state = True
            
            await self.update_sensor_platform_and_data(res["data"])

            self.update_interval = timedelta(seconds=int(res["data"]["settings"]["update_interval"]))

            self.firmware_version = f'{res["data"]["info"]["kernel_version"]} {res["data"]["info"]["os_version"]}'
            self.name = f'{res["data"]["info"]["system_name"]}'
            self.model = f'{res["data"]["info"]["system_name"]}'
        except (ConnectionRefusedError, TimeoutError, socket.timeout):
            self._power_state = False
            return False
        except Exception as e:
            _LOGGER.exception(e)
            self._power_state = False
            return False
        finally:
            sock.close()
            return res
    
    async def update_sensor_platform_and_data(self, data):
        self.set_memory_data(data)
        cpu_change = self.set_cpu_data(data)
        if  cpu_change:
            await self._hass.config_entries.async_forward_entry_unload( # reload sensor platform to reload new sensors if one if the datapoints has changed
                self.sensorConfigEntry, "sensor"
            )
            self.cpu_list = data["state"]["cpu"]["cores"]
            await self._hass.config_entries.async_forward_entry_setup(
                self.sensorConfigEntry, "sensor"
            )

    def set_cpu_data(self, data):
        ret = False
        if (collections.Counter(self.cpu_list.keys()) != collections.Counter(data["state"]["cpu"]["cores"].keys())) and self.sensorConfigEntry != None: # if list of cpu cores changed, update sensor platform to load new sensors
            ret = True
        else:
            self.cpu_list = data["state"]["cpu"]["cores"]

        self.average_cpu_load = data["state"]["cpu"]["average"]
        return ret

    def set_memory_data(self, data):
        self.memory["memory"]["total"] = "{:.1f}".format(float(data["info"]["total_memory"]) / (2**20))
        self.memory["swap"]["total"] = "{:.1f}".format(float(data["info"]["total_swap"]) / (2**20))
        self.memory["memory"]["used"] = round((float(data["state"]["used_memory"]) / (2**20)) / float(self.memory["memory"]["total"]) * 100)
        self.memory["swap"]["used"] = round((float(data["state"]["used_swap"]) / (2**20)) / float(self.memory["swap"]["total"]) * 100)

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
