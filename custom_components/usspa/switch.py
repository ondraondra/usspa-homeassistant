
from __future__ import annotations
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, get_meta, category_for

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

class BaseSwitch(CoordinatorEntity, SwitchEntity):
    KEY = ""
    def __init__(self, coordinator, entry: ConfigEntry, client) -> None:
        super().__init__(coordinator)
        self._client = client
        self._entry = entry
        meta = get_meta(self.KEY)
        self._attr_unique_id = f"{entry.entry_id}_switch_{self.KEY.lower()}"
        if meta["name"]:
            self._attr_name = f"USSPA {meta['name']}"
        if meta["icon"]:
            self._attr_icon = meta["icon"]
        self._attr_entity_registry_enabled_default = meta["enabled_default"]
        cat = category_for(self.KEY)
        if cat is not None:
            self._attr_entity_category = cat

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

class USSPABubblesSwitch(BaseSwitch):
    KEY = "Pump3"
    @property
    def is_on(self) -> bool:
        return str((self.coordinator.data.get("Pump3") or {}).get("value","")) == "1"
    async def async_turn_on(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetPump3;Pump3,1")
        await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetPump3;Pump3,0")
        await self.coordinator.async_request_refresh()

class USSPAHeatBlockingSwitch(BaseSwitch):
    KEY = "SafeMode"
    @property
    def is_on(self) -> bool:
        return str((self.coordinator.data.get("SafeMode") or {}).get("value","")) == "1"
    async def async_turn_on(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetSafeMode;SafeMode,1")
        await self.coordinator.async_request_refresh()
    async def async_turn_off(self, **kwargs) -> None:
        await self.hass.async_add_executor_job(self._client.send_command, "SetSafeMode;SafeMode,0")
        await self.coordinator.async_request_refresh()
