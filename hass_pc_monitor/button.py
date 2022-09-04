"""Platform for button integration."""
import logging

from .const import DOMAIN
from .entity import BaseEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.button import ButtonEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry: ConfigEntry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    connection = hass.data[DOMAIN][config_entry.entry_id]
    connection.configEntry = config_entry

    new_devices = []
    for command in connection.command_list.keys():
        new_devices.append(CommandButton(connection, command))

    async_add_entities(new_devices)


class CommandButton(BaseEntity, ButtonEntity):
    """Representation of a Sensor."""

    def __init__(self, connection, command_name):
        """Initialize the sensor."""
        super().__init__(connection)
        self._command_name = command_name

        self._attr_unique_id = f"{self._connection.connection_id}_command_{command_name}"

        self._attr_name = f"{self._connection.name} {self._connection.command_list[command_name]['display_name']} Command"

    def press(self):
        self._connection.command_button_clicked(self._command_name)