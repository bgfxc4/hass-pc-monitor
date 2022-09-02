"""Base Entity Class"""
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class BaseEntity(CoordinatorEntity):
    """Base representation of a Hello World Sensor."""

    #should_poll = False

    def __init__(self, connection):
        """Initialize the sensor."""
        super().__init__(connection)
        self._connection = connection

    @property
    def device_info(self):
        """Return information to link this entity with the correct device."""
        return DeviceInfo({
            "identifiers": {(DOMAIN, self._connection.connection_id)},
            "name": self._connection.name,
            "sw_version": self._connection.firmware_version,
            "manufacturer": self._connection.manufacturer,
            "model": self._connection.model
        })

    @property
    def available(self) -> bool:
        return self._connection.power_state