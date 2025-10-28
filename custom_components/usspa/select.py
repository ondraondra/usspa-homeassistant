
from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from typing import Any

from .const import DOMAIN

OPTIONS = ["off", "low", "high"]
TO_LEVEL = {"off": "0", "low": "1", "high": "2"}
FROM_LEVEL = {"0": "off", "1": "low", "2": "high"}

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]

    if "Pump1" in coordinator.data:
        async_add_entities([USSPAStreamSpeedSelect(coordinator, entry, client)])

class USSPAStreamSpeedSelect(CoordinatorEntity, SelectEntity):
    _attr_has_entity_name = True
    _attr_name = "USSPA Stream Speed"
    _attr_options = OPTIONS

    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_select_stream_speed"
        self._entry = entry
        self._serial = entry.data.get("serial")

    @property
    def device_info(self):
        model = (self.coordinator.data.get('Model') or {}).get('value') if isinstance(self.coordinator.data, dict) else None
        swv = (self.coordinator.data.get('SwVer') or {}).get('value') if isinstance(self.coordinator.data, dict) else None
        return {
            "identifiers": {("usspa", self._serial)},
            "manufacturer": "USSPA",
            "model": model or "Spa Controller",
            "sw_version": swv,
            "name": self._entry.title,
            "serial_number": self._serial,
        }

    @property
    def current_option(self) -> str | None:
        v = str((self.coordinator.data.get("Pump1") or {}).get("value", ""))
        return FROM_LEVEL.get(v, "off")

    async def async_select_option(self, option: str) -> None:
        level = TO_LEVEL.get(option, "0")
        cmd = f"SetPump1;Pump1,{level}"
        await self.hass.async_add_executor_job(self._client.send_command, cmd)
        await self.coordinator.async_request_refresh()
