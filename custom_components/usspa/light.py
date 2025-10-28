
from __future__ import annotations

from homeassistant.components.light import LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    client = data["client"]

    if "Light1" in coordinator.data:
        ents = [USSPALight1(coordinator, entry, client)]
        if 'Light2' in coordinator.data:
            ents.append(USSPALight2(coordinator, entry, client))
        async_add_entities(ents)

class USSPALight1(CoordinatorEntity, LightEntity):
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
    _attr_name = "USSPA Light 1"

    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._entry = entry
        self._serial = entry.data.get('serial')
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_light_light1"

    @property
    def is_on(self) -> bool:
        val = str((self.coordinator.data.get("Light1") or {}).get("value", ""))
        return val == "1"

    async def async_turn_on(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetLight1;Light1,1")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetLight1;Light1,0")
        await self.coordinator.async_request_refresh()


class USSPALight2(CoordinatorEntity, LightEntity):
    _attr_has_entity_name = True
    _attr_name = "USSPA Light 2"

    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._attr_unique_id = f"{entry.entry_id}_light_light2"
        self._entry = entry
        self._serial = entry.data.get("serial")
        self._attr_entity_registry_enabled_default = False

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
        val = str((self.coordinator.data.get("Light2") or {}).get("value", ""))
        return val == "1"

    async def async_turn_on(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetLight2;Light2,1")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetLight2;Light2,0")
        await self.coordinator.async_request_refresh()
