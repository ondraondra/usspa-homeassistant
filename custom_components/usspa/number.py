
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]

    if "ReqTemp" in coordinator.data:
        async_add_entities([USSPATempSetpointNumber(coordinator, entry, client)])

class USSPATempSetpointNumber(CoordinatorEntity, NumberEntity):
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
    _attr_name = "USSPA Temperature Setpoint"
    _attr_native_step = 0.5
    _attr_native_min_value = 5.0
    _attr_native_max_value = 42.0
    _attr_native_unit_of_measurement = "°C"
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._serial = entry.data.get('serial')
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_number_reqtemp"

    @property
    def native_value(self) -> float | None:
        val = (self.coordinator.data.get("ReqTemp") or {}).get("value")
        try:
            return float(val) if val is not None else None
        except (ValueError, TypeError):
            return None

    async def async_set_native_value(self, value: float) -> None:
        # Clamp and send with one decimal
        val = max(min(value, self._attr_native_max_value), self._attr_native_min_value)
        cmd = f"SetReqTemp;ReqTemp,{val:.1f}"
        await self.hass.async_add_executor_job(self._client.send_command, cmd)
        await self.coordinator.async_request_refresh()
