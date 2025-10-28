from __future__ import annotations

import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import USSPAClient

_LOGGER = logging.getLogger(__name__)


def parse_csv_to_dict(csv_line: str) -> Dict[str, Dict[str, Any]]:
    """Parse 'Key,Value,Time;Key2,Value2,Time;...;#' into a dict."""
    out: Dict[str, Dict[str, Any]] = {}
    if not csv_line:
        return out
    if csv_line.endswith("#"):
        csv_line = csv_line[:-1]

    for part in csv_line.split(";"):
        if not part:
            continue
        fields = part.split(",")
        key = fields[0]
        value = fields[1] if len(fields) > 1 else ""
        ts = fields[2] if len(fields) > 2 else None

        # Normalize timestamps → timezone-aware ISO (UTC)
        if key in (
            "LastConn",
            "ActDateTime",
            "ProductionDate",
            "SpaInstallDate",
            "EnergyResetDateTime",
            "TmpEnergyResetDateTime",
        ) and ts:
            try:
                dt = datetime.fromisoformat(ts.replace(" ", "T"))
                value = dt.replace(tzinfo=timezone.utc).isoformat()
            except Exception:
                _LOGGER.debug("Timestamp parse failed for %s=%r", key, ts)

        # Convert runtimes seconds → hours (one decimal)
        if key in ("OzoneRuntime", "Pump3Runtime"):
            try:
                value = round(int(value) / 3600, 1)
            except Exception:
                _LOGGER.debug("Runtime conversion failed for %s=%r", key, value)

        out[key] = {"value": value, "ts": ts}
    return out


class USSPADataCoordinator(DataUpdateCoordinator[Dict[str, Dict[str, Any]]]):
    def __init__(self, hass: HomeAssistant, client: USSPAClient, scan_interval: int) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="USSPA Coordinator",
            update_interval=timedelta(seconds=scan_interval),
        )
        self.client = client
        self._logged_in = False

    async def _async_update_data(self) -> Dict[str, Dict[str, Any]]:
        def _fetch():
            if not self._logged_in:
                self.client.login()
                self._logged_in = True
            state = self.client.get_state()
            return parse_csv_to_dict(state)

        return await self.hass.async_add_executor_job(_fetch)
