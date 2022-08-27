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
    print("sensor setup entry")
    """Add sensors for passed config_entry in HA."""
    connection = hass.data[DOMAIN][config_entry.entry_id]

    new_devices = []
    for cpu in connection.cpu_list.keys():
        new_devices.append(CPULoadSensor(connection, cpu))

    new_devices.append(AverageCPULoadSensor(connection))
    async_add_entities(new_devices)


class CPULoadSensor(BaseEntity, SensorEntity):
    """Representation of a Sensor."""

    device_class = DEVICE_CLASS_POWER_FACTOR
    unit_of_measurement = PERCENTAGE
    icon = "mdi:cpu-64-bit"

    def __init__(self, connection, cpu_name):
        """Initialize the sensor."""
        super().__init__(connection)
        self._cpu_name = cpu_name

        self._attr_unique_id = f"{self._connection.connection_id}_cpu_load_{cpu_name}"

        self._attr_name = f"{self._connection.name} {cpu_name} Load"


    @property
    def state(self):
        """Return the state of the sensor."""
        return round(self._connection.cpu_list[self._cpu_name])


class AverageCPULoadSensor(BaseEntity, SensorEntity):
    """Representation of a Sensor."""

    device_class = DEVICE_CLASS_POWER_FACTOR
    unit_of_measurement = PERCENTAGE
    icon = "mdi:cpu-64-bit"

    def __init__(self, connection):
        """Initialize the sensor."""
        super().__init__(connection)

        self._attr_unique_id = f"{self._connection.connection_id}_cpu_load_average"

        self._attr_name = f"{self._connection.name} Average CPU Load"


    @property
    def state(self):
        """Return the state of the sensor."""
        return round(self._connection.average_cpu_load)