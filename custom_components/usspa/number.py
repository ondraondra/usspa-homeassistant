
from __future__ import annotations
from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, get_meta, category_for

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]
    if "ReqTemp" in coordinator.data:
        async_add_entities([USSPATempSetpoint(coordinator, entry, client)])

class USSPATempSetpoint(CoordinatorEntity, NumberEntity):
    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._entry = entry
        meta = get_meta("ReqTemp")
        self._attr_unique_id = f"{entry.entry_id}_number_reqtemp"
        self._attr_mode = NumberMode.BOX
        self._attr_native_step = 0.5
        self._attr_native_min_value = 5.0
        self._attr_native_max_value = 40.0
        if meta["name"]:
            self._attr_name = f"USSPA {meta['name']}"
        if meta["icon"]:
            self._attr_icon = meta["icon"]
        self._attr_entity_registry_enabled_default = meta["enabled_default"]
        cat = category_for("ReqTemp")
        if cat is not None:
            self._attr_entity_category = cat

    @property
    def native_unit_of_measurement(self):
        return "°C"

    @property
    def native_value(self):
        try:
            return float((self.coordinator.data.get("ReqTemp") or {}).get("value"))
        except Exception:
            return None

    async def async_set_native_value(self, value: float) -> None:
        cmd = f"SetReqTemp;ReqTemp,{value:.1f}"
        await self.hass.async_add_executor_job(self._client.send_command, cmd)
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
