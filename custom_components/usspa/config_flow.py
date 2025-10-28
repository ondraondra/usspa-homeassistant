
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from .const import DOMAIN, DEFAULT_BASE_URL, DEFAULT_SCAN_INTERVAL

DATA_SCHEMA = vol.Schema({
    vol.Required("serial"): str,
    vol.Required("password"): str,
    vol.Optional("name", default=""): str,
    vol.Optional("base_url", default=DEFAULT_BASE_URL): str,
})

OPTIONS_SCHEMA = vol.Schema({
    vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): int,
})

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA)
        title = user_input.get("name") or f"USSPA {user_input['serial']}"
        return self.async_create_entry(title=title, data=user_input)

    async def async_get_options_flow(self, config_entry):
        return OptionsFlow(config_entry)

class OptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry):
        self.entry = entry
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(step_id="init", data_schema=OPTIONS_SCHEMA)
