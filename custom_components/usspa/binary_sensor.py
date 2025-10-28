
from __future__ import annotations
from typing import Any
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, get_meta, category_for

BIN_KEYS = ["HeaterState","FiltrState","Pump2","OffMode","Light2"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]
    ents = []
    for key in BIN_KEYS:
        if key in coordinator.data:
            ents.append(USSPABinary(coordinator, entry, client, key))
    async_add_entities(ents)

class USSPABinary(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, entry: ConfigEntry, client, key: str) -> None:
        super().__init__(coordinator)
        self._client = client
        self._entry = entry
        self._key = key
        meta = get_meta(key)
        self._attr_unique_id = f"{entry.entry_id}_bin_{key.lower()}"
        if meta["name"]:
            self._attr_name = f"USSPA {meta['name']}"
        if meta["icon"]:
            self._attr_icon = meta["icon"]
        self._attr_entity_registry_enabled_default = meta["enabled_default"]
        cat = category_for(key)
        if cat is not None:
            self._attr_entity_category = cat

    @property
    def is_on(self) -> bool:
        val = str((self.coordinator.data.get(self._key) or {}).get("value",""))
        return val in ("1","true","on","2")  # treat "2" as on for some states

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
