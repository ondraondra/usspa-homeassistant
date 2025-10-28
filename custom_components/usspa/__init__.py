
from __future__ import annotations

import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, DEFAULT_SCAN_INTERVAL
from .api import USSPAClient
from .coordinator import USSPADataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BINARY_SENSOR, Platform.SWITCH, Platform.NUMBER, Platform.LIGHT, Platform.SELECT]

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    client = USSPAClient(
        serial=entry.data["serial"],
        password=entry.data["password"],
        base_url=entry.data.get("base_url") or "https://in.usspa.cz",
    )
    coordinator = USSPADataUpdateCoordinator(hass, client, timedelta(seconds=entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)))
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"client": client, "coordinator": coordinator}

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Service for arbitrary commands
    async def async_send_command(call):
        cmd = call.data.get("command")
        resp = await hass.async_add_executor_job(client.send_command, cmd)
        await coordinator.async_request_refresh()

    hass.services.async_register(DOMAIN, "send_command", async_send_command)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
