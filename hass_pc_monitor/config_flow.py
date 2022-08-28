"""Config flow for Hello World integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import DOMAIN  # pylint:disable=unused-import
from .monitorConnection import MonitorConnection

import hashlib

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({("host"): str, ("port"): int, ("password"): str})


async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    h = hashlib.new("sha512", data["password"].encode('utf-8'))
    data["password"] = h.hexdigest()
    connection = MonitorConnection(hass, data["host"], data["port"], data["password"])

    result = await connection.get_state_from_device()
    if not result:
        raise CannotConnect

    if result["status"] == 401:
        raise InvalidAuth
    if result["status"] != 200:
        raise Exception
    return {"title": connection.name}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except KeyError:
                errors["base"] = "incomplete_form"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""

class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""

class UnknownError(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
