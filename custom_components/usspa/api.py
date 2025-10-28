
from __future__ import annotations

import requests
from typing import Any, Dict, Tuple
import threading

def parse_triplet_payload(text: str) -> dict[str, dict[str, Any]]:
    """Parse 'name,value,upDate;name2,value2,upDate2;...' into a dict.
    Some entries may be 'key:value' style or missing timestamps.
    Return structure: { name: { 'value': <str>, 'updated_at': <str|None> } }
    """
    out: dict[str, dict[str, Any]] = {}
    text = (text or "").strip().strip(";")
    if not text:
        return out
    # split by ';' but ignore trailing '#'
    parts = [p for p in text.split(';') if p and p != '#']
    for p in parts:
        if ',' in p:
            # name,value[,upDate]
            first, *rest = p.split(',')
            name = first
            value = rest[0] if len(rest) >= 1 else ""
            updated = rest[1] if len(rest) >= 2 else None
            out[name] = {"value": value, "updated_at": updated}
        elif ':' in p:
            # key:value form
            k, v = p.split(':', 1)
            out[k] = {"value": v, "updated_at": None}
        else:
            # just a token
            out[p] = {"value": "", "updated_at": None}
    return out

class USSPAClient:
    def __init__(self, serial: str, password: str, base_url: str = "https://in.usspa.cz") -> None:
        self._serial = serial
        self._password = password
        self._base = base_url.rstrip("/")
        self._session = requests.Session()
        self._lock = threading.Lock()

    def _login(self) -> None:
        self._session.get(f"{self._base}/commands.json", timeout=15)
        login_data = {"data": f"Login,{self._serial},{self._password}"}
        self._session.post(f"{self._base}/app/", data=login_data, timeout=15)

    def get_raw(self, command: str = "GetCommand") -> str:
        with self._lock:
            self._login()
            payload = f"data=SN%3A{self._serial}%3BCmd,{command}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            resp = self._session.post(f"{self._base}/app/", data=payload, headers=headers, timeout=20)
            resp.raise_for_status()
            return resp.text

    def get_data(self, command: str = "GetCommand") -> dict[str, dict[str, Any]]:
        raw = self.get_raw(command=command)
        return parse_triplet_payload(raw)

    def send_command(self, raw_command: str) -> dict[str, Any]:
        with self._lock:
            self._login()
            data = {"data": f"SN:{self._serial};Cmd,{raw_command}"}
            resp = self._session.post(f"{self._base}/app/", data=data, timeout=20)
            resp.raise_for_status()
            txt = resp.text.strip()
        return parse_triplet_payload(txt)
