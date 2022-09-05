"""A demonstration 'hub' that connects several devices."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (DataUpdateCoordinator)

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

    command_list = {}

    memory = {
        "memory": {"total": 0, "used": 0},
        "swap": {"total": 0, "used": 0}
    }

    isFirstDataLoad = True
    configEntry: ConfigEntry = None

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
            await self.update_button_platform_and_data(res["data"])

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
        if cpu_change:
            #self.cpu_list = data["state"]["cpu"]["cores"]
            await self.reload_config_entry("sensor")

    def set_cpu_data(self, data):
        ret = False
        if (collections.Counter(self.cpu_list.keys()) != collections.Counter(data["state"]["cpu"]["cores"].keys())) and self.configEntry != None: # if list of cpu cores changed, update sensor platform to load new sensors
            ret = True
        self.cpu_list = data["state"]["cpu"]["cores"]

        self.average_cpu_load = data["state"]["cpu"]["average"]
        return ret

    def set_memory_data(self, data):
        self.memory["memory"]["total"] = "{:.1f}".format(float(data["info"]["total_memory"]) / (2**20))
        self.memory["swap"]["total"] = "{:.1f}".format(float(data["info"]["total_swap"]) / (2**20))
        self.memory["memory"]["used"] = round((float(data["state"]["used_memory"]) / (2**20)) / float(self.memory["memory"]["total"]) * 100)
        self.memory["swap"]["used"] = round((float(data["state"]["used_swap"]) / (2**20)) / float(self.memory["swap"]["total"]) * 100)

    async def update_button_platform_and_data(self, data):
        command_change = self.set_command_data(data)
        if command_change and self.configEntry != None:
            #self.command_list = data["settings"]["commands"]
            await self.reload_config_entry("button")
    
    def set_command_data(self, data):
        ret = False
        if len(data["settings"]["commands"].keys()) != len(self.command_list.keys()):
            ret = True
        else:
            for c in data["settings"]["commands"]:# if list of commands changed, update button platform to load new buttons
                if c not in self.command_list:
                    ret = True
                    break
                new_c = data["settings"]["commands"][c]
                old_c = self.command_list[c]
                if (new_c["display_name"] != old_c.get("display_name", "") or new_c["args"] != old_c.get("args", "") or new_c["command"] != old_c.get("command", "")):
                    ret = True
                    break
        self.command_list = data["settings"]["commands"]
        return ret


    async def reload_config_entry(self, platform_name):
        await self._hass.config_entries.async_forward_entry_unload( # reload sensor platform to reload new sensors if one if the datapoints has changed
            self.configEntry, platform_name
        )
        await self._hass.config_entries.async_forward_entry_setup(
            self.configEntry, platform_name
        )

    def command_button_clicked(self, command_name):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.settimeout(1)
            sock.connect(self.server_address)
            message = {
                "token": "exec_command",
                "password": self._password,
                "command_name": command_name
            }
            sock.sendall(bytes(json.dumps(message)+"\n\n", encoding="utf-8"))

        except Exception as e:
            _LOGGER.exception(e)
            return False

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
