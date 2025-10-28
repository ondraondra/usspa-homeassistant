
from __future__ import annotations

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]

    # Only add if SafeMode present in data
    if "SafeMode" in coordinator.data:
        async_add_entities([USSPAEnableHeatBlockingButton(coordinator, entry, client), USSPADisableHeatBlockingButton(coordinator, entry, client)])

class USSPAEnableHeatBlockingButton(CoordinatorEntity, ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = "USSPA Enable Heat Blocking"

    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_button_enable_heat_blocking"
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

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetSafeMode;SafeMode,1")
        await self.coordinator.async_request_refresh()


class USSPADisableHeatBlockingButton(CoordinatorEntity, ButtonEntity):
    _attr_has_entity_name = True
    _attr_name = "USSPA Disable Heat Blocking"

    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_button_disable_heat_blocking"
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

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetSafeMode;SafeMode,0")
        await self.coordinator.async_request_refresh()
