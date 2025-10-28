
from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime, timezone
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN, MAPPING

TIME_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",  # some are dates only
    "%H:%M",     # time-of-day strings
]

def parse_timestamp(value: str) -> Optional[datetime]:
    if not value or value in ("0000-00-00 00:00:00",):
        return None
    for fmt in TIME_FORMATS:
        try:
            dt = datetime.strptime(value, fmt)
            # Make timezone-aware (UTC) to satisfy HA timestamp expectations
            return dt.replace(tzinfo=timezone.utc)
        except Exception:
            continue
    return None

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    entities = []
    for key in coordinator.data.keys():
        meta = MAPPING.get(key, {})
        platform = meta.get("platform", "sensor")
        if platform not in ("sensor",):  # others handled in their own platforms
            continue
        entities.append(USSPASensor(coordinator, entry, key, meta))
    async_add_entities(entities)

class USSPASensor(CoordinatorEntity, SensorEntity):
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
        self._device_class = meta.get("device_class")
        self._unit = meta.get("unit")
        self._attr_unique_id = f"{entry.entry_id}_sensor_{key}"
        self._attr_entity_registry_enabled_default = bool(meta)

    @property
    def name(self) -> str:
        return f"USSPA {self._friendly}"

    @property
    def device_class(self) -> str | None:
        # If mapping defines device class, return it
        if self._device_class:
            return self._device_class
        # Infer temperature for some keys
        if self._key.lower().endswith("temp") or self._key in ("FanStart", "FanStop"):
            return "temperature"
        # Infer timestamp by value
        val = (self.coordinator.data.get(self._key) or {}).get("value")
        if isinstance(val, str) and parse_timestamp(val):
            return "timestamp"
        return None

    @property
    def native_unit_of_measurement(self) -> str | None:
        if self._unit:
            return self._unit
        if self.device_class == "temperature":
            return "°C"
        if self._key.endswith("Runtime"):
            return "h"
        return None

    @property
    def native_value(self) -> Any:
        d = self.coordinator.data.get(self._key) or {}
        val = d.get("value")

        # Convert runtimes (values are seconds) → hours
        if self._key.endswith("Runtime"):
            try:
                sec = float(val)
                return round(sec / 3600.0, 2)
            except (TypeError, ValueError):
                return None

        # Temperature-like numeric
        if self.device_class == "temperature":
            try:
                return float(val)
            except (TypeError, ValueError):
                # some temp-like values may be strings like "41.0"
                try:
                    return float(str(val))
                except Exception:
                    return None

        # Timestamp
        if self.device_class == "timestamp":
            return parse_timestamp(val)

        # Default: return raw
        return val
