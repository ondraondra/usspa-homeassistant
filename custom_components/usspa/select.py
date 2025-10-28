
from __future__ import annotations
from typing import Any
from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, get_meta, category_for

OPTIONS = ["off", "low", "high"]
TO_LEVEL = {"off":"0","low":"1","high":"2"}
FROM_LEVEL = {"0":"off","1":"low","2":"high"}

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]
    if "Pump1" in coordinator.data:
        async_add_entities([USSPAStreamSpeedSelect(coordinator, entry, client)])

class USSPAStreamSpeedSelect(CoordinatorEntity, SelectEntity):
    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._entry = entry
        self._attr_options = OPTIONS
        meta = get_meta("Pump1")
        self._attr_unique_id = f"{entry.entry_id}_select_pump1"
        if meta["name"]:
            self._attr_name = f"USSPA {meta['name']}"
        if meta["icon"]:
            self._attr_icon = meta["icon"]
        self._attr_entity_registry_enabled_default = meta["enabled_default"]
        cat = category_for("Pump1")
        if cat is not None:
            self._attr_entity_category = cat

    @property
    def current_option(self) -> str | None:
        v = str((self.coordinator.data.get("Pump1") or {}).get("value",""))
        return FROM_LEVEL.get(v, "off")

    async def async_select_option(self, option: str) -> None:
        level = TO_LEVEL.get(option, "0")
        await self.hass.async_add_executor_job(self._client.send_command, f"SetPump1;Pump1,{level}")
        await self.coordinator.async_request_refresh()

    @property
    def device_info(self):
        model = (self.coordinator.data.get('Model') or {}).get('value')
        swv = (self.coordinator.data.get('SwVer') or {}).get('value')
        return {
            "identifiers": {("usspa", self._entry.data["serial"])},
            "manufacturer": "USSPA",
            "model": model or "Spa Controller",
            "sw_version": swv,
            "name": self._entry.title,
            "serial_number": self._entry.data["serial"],
        }
