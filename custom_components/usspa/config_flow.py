
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN, CONF_SERIAL, CONF_PASSWORD, CONF_BASE_URL, DEFAULT_BASE_URL

DATA_SCHEMA = vol.Schema({
    vol.Optional('name', default=''): str,
    vol.Required(CONF_SERIAL): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Optional(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
})

class USSPAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            # Basic sanity: try a single fetch
            serial = user_input[CONF_SERIAL]
            password = user_input[CONF_PASSWORD]
            base_url = user_input.get(CONF_BASE_URL, DEFAULT_BASE_URL)
            # Defer API import to avoid circulars
            from .api import USSPAClient
            client = USSPAClient(serial=serial, password=password, base_url=base_url)
            try:
                data = await self.hass.async_add_executor_job(client.get_data)
                if not isinstance(data, dict):
                    errors["base"] = "cannot_connect"
                else:
                    await self.async_set_unique_id(f"{DOMAIN}_{serial}")
                    self._abort_if_unique_id_configured()
                    title = user_input.get('name') or f'USSPA {serial}'
                    return self.async_create_entry(title=title, data=user_input)
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)


from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol

class USSPAOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        self.entry = entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.entry.options or {}
        schema = vol.Schema({
            vol.Optional("scan_interval", default=current.get("scan_interval", 30)): int,
        })
        return self.async_show_form(step_id="init", data_schema=schema)

async def async_get_options_flow(config_entry: config_entries.ConfigEntry):
    return USSPAOptionsFlow(config_entry)
