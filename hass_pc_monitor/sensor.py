"""Platform for sensor integration."""

from homeassistant.const import (
    PERCENTAGE,
    DEVICE_CLASS_POWER_FACTOR
)
import logging

from .const import DOMAIN
from .entity import BaseEntity

from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    connection = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    new_devices.append(CPULoadSensor(connection))
    new_devices.append(TestLoadSensor(connection))
    async_add_entities(new_devices)


class CPULoadSensor(BaseEntity, SensorEntity):
    """Representation of a Sensor."""

    device_class = DEVICE_CLASS_POWER_FACTOR
    unit_of_measurement = PERCENTAGE

    def __init__(self, connection):
        """Initialize the sensor."""
        super().__init__(connection)

        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._connection.connection_id}_cpu_load"

        # The name of the entity
        self._attr_name = f"{self._connection.name} CPU Load"

        self._state = self._connection.cpu_load


    @property
    def state(self):
        """Return the state of the sensor."""
        return self._connection.cpu_load

class TestLoadSensor(BaseEntity, SensorEntity):
    """Representation of a Sensor."""

    device_class = DEVICE_CLASS_POWER_FACTOR
    unit_of_measurement = PERCENTAGE

    def __init__(self, connection):
        """Initialize the sensor."""
        super().__init__(connection)

        # As per the sensor, this must be a unique value within this domain. This is done
        # by using the device ID, and appending "_battery"
        self._attr_unique_id = f"{self._connection.connection_id}_test"

        # The name of the entity
        self._attr_name = f"{self._connection.name} Test"

        self._state = self._connection.cpu_load


    @property
    def state(self):
        """Return the state of the sensor."""
        return 15