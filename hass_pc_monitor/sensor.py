"""Platform for sensor integration."""

from homeassistant.const import (
    PERCENTAGE,
    DATA_GIBIBYTES
)
import logging

from .const import DOMAIN
from .entity import BaseEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import SensorEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry: ConfigEntry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    connection = hass.data[DOMAIN][config_entry.entry_id]
    connection.configEntry = config_entry

    new_devices = []
    for cpu in connection.cpu_list.keys():
        new_devices.append(CPULoadSensor(connection, cpu))

    new_devices.append(AverageCPULoadSensor(connection))
    new_devices.append(MemoryTotalSensor(connection, MemoryType.MEMORY))
    new_devices.append(MemoryUsedSensor(connection, MemoryType.MEMORY))
    new_devices.append(MemoryTotalSensor(connection, MemoryType.SWAP))
    new_devices.append(MemoryUsedSensor(connection, MemoryType.SWAP))
    async_add_entities(new_devices)


class CPULoadSensor(BaseEntity, SensorEntity):
    """Representation of a Sensor."""

    unit_of_measurement = PERCENTAGE
    icon = "mdi:cpu-64-bit"
    state_class = "measurement"

    def __init__(self, connection, cpu_name):
        """Initialize the sensor."""
        super().__init__(connection)
        self._cpu_name = cpu_name

        self._attr_unique_id = f"{self._connection.connection_id}_cpu_load_{cpu_name}"

        self._attr_name = f"{self._connection.name} {cpu_name} Load"


    @property
    def state(self):
        """Return the state of the sensor."""
        if (self._connection.power_state):
            return round(self._connection.cpu_list[self._cpu_name])
        else:
            return None


class AverageCPULoadSensor(BaseEntity, SensorEntity):
    """Representation of a Sensor."""

    unit_of_measurement = PERCENTAGE
    icon = "mdi:cpu-64-bit"
    state_class = "measurement"

    def __init__(self, connection):
        """Initialize the sensor."""
        super().__init__(connection)

        self._attr_unique_id = f"{self._connection.connection_id}_cpu_load_average"

        self._attr_name = f"{self._connection.name} Average CPU Load"


    @property
    def state(self):
        """Return the state of the sensor."""
        if (self._connection.power_state):
            return round(self._connection.average_cpu_load)
        else:
            return None

class MemoryType():
    SWAP = "Swap"
    MEMORY = "Memory"

class MemoryTotalSensor(BaseEntity, SensorEntity):
    """Representation of a Sensor."""

    unit_of_measurement = DATA_GIBIBYTES
    icon = "mdi:memory"
    state_class = "total"

    def __init__(self, connection, memoryType):
        """Initialize the sensor."""
        super().__init__(connection)
        self.memoryType = memoryType
        self._attr_unique_id = f"{self._connection.connection_id}_{memoryType.lower()}_total"

        self._attr_name = f"{self._connection.name} {memoryType} Total"


    @property
    def state(self):
        """Return the state of the sensor."""
        if (self._connection.power_state):
            return self._connection.memory[self.memoryType.lower()]["total"]
        else:
            return None

class MemoryUsedSensor(BaseEntity, SensorEntity):
    """Representation of a Sensor."""

    unit_of_measurement = PERCENTAGE
    icon = "mdi:memory"
    state_class = "measurement"

    def __init__(self, connection, memoryType):
        """Initialize the sensor."""
        super().__init__(connection)
        self.memoryType = memoryType
        self._attr_unique_id = f"{self._connection.connection_id}_{memoryType.lower()}_used"

        self._attr_name = f"{self._connection.name} {memoryType} Used"


    @property
    def state(self):
        """Return the state of the sensor."""
        if (self._connection.power_state):
            return self._connection.memory[self.memoryType.lower()]["used"]
        else:
            return None