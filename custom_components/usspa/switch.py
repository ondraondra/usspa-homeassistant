
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]

    entities = []
    if "Pump3" in coordinator.data:
        entities.append(USSPABubblesSwitch(coordinator, entry, client))
    if "SafeMode" in coordinator.data:
        entities.append(USSPAHeatBlockingSwitch(coordinator, entry, client))
    async_add_entities(entities)

class USSPABubblesSwitch(CoordinatorEntity, SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = "USSPA Bubbles"

    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_switch_bubbles"
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
    def is_on(self) -> bool:
        val = str((self.coordinator.data.get("Pump3") or {}).get("value", ""))
        return val == "1"

    async def async_turn_on(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetPump3;Pump3,1")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetPump3;Pump3,0")
        await self.coordinator.async_request_refresh()

class USSPAHeatBlockingSwitch(CoordinatorEntity, SwitchEntity):
    _attr_has_entity_name = True
    _attr_name = "USSPA Heat blocking"

    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_switch_heat_blocking"
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
    def is_on(self) -> bool:
        val = str((self.coordinator.data.get("SafeMode") or {}).get("value", ""))
        return val == "1"

    async def async_turn_on(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetSafeMode;SafeMode,1")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetSafeMode;SafeMode,0")
        await self.coordinator.async_request_refresh()
