
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any, Dict
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import USSPAClient

_LOGGER = logging.getLogger(__name__)

class USSPADataUpdateCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    def __init__(self, hass: HomeAssistant, client: USSPAClient, interval: timedelta) -> None:
        super().__init__(hass, _LOGGER, name="USSPA Coordinator", update_interval=interval)
        self._client = client

    async def _async_update_data(self) -> Dict[str, Any]:
        try:
            return await self.hass.async_add_executor_job(self._client.get_data)
        except Exception as exc:
            raise UpdateFailed(str(exc)) from exc
