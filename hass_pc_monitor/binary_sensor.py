"""Platform for sensor integration."""
from homeassistant.const import (
    DEVICE_CLASS_POWER
)
from homeassistant.components.binary_sensor import BinarySensorEntity

import logging

from .const import DOMAIN
from .entity import BaseEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    connection = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    new_devices.append(PowerStateSensor(connection))
    async_add_entities(new_devices)

class PowerStateSensor(BaseEntity, BinarySensorEntity):
    """Representation of a Sensor."""
    device_class = DEVICE_CLASS_POWER

    def __init__(self, connection):
        """Initialize the sensor."""
        super().__init__(connection)

        self._attr_unique_id = f"{self._connection.connection_id}_power_state"

        # The name of the entity
        self._attr_name = f"{self._connection.name} Power State"
    
    @property
    def is_on(self):
        return self._connection.power_state