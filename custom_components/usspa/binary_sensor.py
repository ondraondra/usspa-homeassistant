
from __future__ import annotations

from typing import Any, Dict
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, MAPPING

BINARY_KEYS = [k for k, v in MAPPING.items() if v.get("platform") == "binary_sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    entities = []
    for key in coordinator.data.keys():
        meta = MAPPING.get(key, {})
        if meta.get("platform") == "binary_sensor" or key in BINARY_KEYS:
            entities.append(USSPABinary(coordinator, entry, key, meta))
    async_add_entities(entities)

class USSPABinary(CoordinatorEntity, BinarySensorEntity):
    @property
    def device_info(self):
        data = self.coordinator.data if hasattr(self, 'coordinator') else {}
        # Attempt to get model & sw_version if available
        model = (data.get('Model') or {}).get('value') if isinstance(data, dict) else None
        swv = (data.get('SwVer') or {}).get('value') if isinstance(data, dict) else None
        serial = getattr(self, '_serial', None)
        # Fallback: try to pull from entry data
        try:
            serial = serial or self._entry.data.get('serial')
        except Exception:
            pass
        return {
            "identifiers": {("usspa", serial)} if serial else {("usspa", self.unique_id)},
            "manufacturer": "USSPA",
            "model": model or "Spa Controller",
            "serial_number": serial,
            "sw_version": swv,
            "name": self._entry.title if hasattr(self, '_entry') else "USSPA",
        }

    _attr_has_entity_name = True

    def __init__(self, coordinator, entry: ConfigEntry, key: str, meta: Dict[str, Any]) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._serial = entry.data.get('serial')
        self._key = key
        self._entry = entry
        self._friendly = meta.get("name", key)
        self._attr_unique_id = f"{entry.entry_id}_binary_{key}"
        self._attr_entity_registry_enabled_default = bool(meta)

    @property
    def name(self) -> str:
        return f"USSPA {self._friendly}"

    @property
    def is_on(self) -> bool:
        d = self.coordinator.data.get(self._key) or {}
        val = str(d.get("value", "")).strip().lower()
        return val in ("1", "true", "on", "yes")
