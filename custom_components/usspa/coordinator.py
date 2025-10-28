
from __future__ import annotations
import csv
from io import StringIO
from datetime import timezone, datetime
from typing import Dict, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .api import USSPAClient
from .const import DEFAULT_SCAN_INTERVAL

def parse_csv_to_dict(csv_line: str) -> Dict[str, Dict[str, Any]]:
    # Input like "Key,Value,Time;Key2,Value2,Time;...;#"
    out: Dict[str, Dict[str, Any]] = {}
    if not csv_line:
        return out
    if csv_line.endswith("#"):
        csv_line = csv_line[:-1]
    parts = csv_line.split(";")
    for p in parts:
        if not p:
            continue
        fields = p.split(",")
        if not fields:
            continue
        key = fields[0]
        value = fields[1] if len(fields) > 1 else ""
        ts = fields[2] if len(fields) > 2 else None
        # normalize timestamps
        if key in ("LastConn","ActDateTime","ProductionDate","SpaInstallDate","EnergyResetDateTime","TmpEnergyResetDateTime"):
            try:
                # treat as naive local? We convert to aware UTC, preserving wall time string
                dt = datetime.fromisoformat(ts.replace(" ", "T"))
                value = dt.replace(tzinfo=timezone.utc).isoformat()
            except Exception:
                pass
        # convert runtimes seconds->hours
        if key in ("OzoneRuntime","Pump3Runtime"):
            try:
                value = round(int(value) / 3600, 1)
            except Exception:
                pass
        out[key] = {"value": value, "ts": ts}
    return out

class USSPADataCoordinator(DataUpdateCoordinator[Dict[str, Dict[str, Any]]]):

    def __init__(self, hass: HomeAssistant, client: USSPAClient, scan_interval: int) -> None:
        super().__init__(
            hass,
            hass.helpers.event.async_track_time_interval.__self__,
            name="USSPA Coordinator",
            update_interval=None,  # we'll schedule manually
        )
        self.client = client
        self._interval = scan_interval

    async def _async_update_data(self) -> Dict[str, Dict[str, Any]]:
        # run in executor
        def _fetch():
            # ensure login once per scheduler restart if needed
            if not hasattr(self, "_logged"):
                self.client.login()
                self._logged = True
            state = self.client.get_state()
            return parse_csv_to_dict(state)

        return await self.hass.async_add_executor_job(_fetch)
