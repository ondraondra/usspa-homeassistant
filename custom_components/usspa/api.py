
from __future__ import annotations
import requests
from typing import Dict, Any

class USSPAClient:
    def __init__(self, base_url: str, serial: str, password: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.serial = serial
        self.password = password
        self.session = requests.Session()

    def _app_url(self) -> str:
        return f"{self.base_url}/app/"
    def _cmd_url(self) -> str:
        return f"{self.base_url}/commands.json"

    def login(self) -> bool:
        # get cookie
        self.session.get(self._cmd_url())
        data = f"data=Login,{self.serial},{self.password}"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        r = self.session.post(self._app_url(), data=data, headers=headers, timeout=20)
        if r.ok and "ErrCode,0" in r.text:
            return True
        return False

    def get_state(self) -> str:
        data = f"data=SN%3A{self.serial}%3BCmd,GetCommand"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        r = self.session.post(self._app_url(), data=data, headers=headers, timeout=20)
        r.raise_for_status()
        return r.text

    def send_command(self, raw: str) -> str:
        # raw like 'SetPump1;Pump1,1'
        data = f"data=SN%3A{self.serial}%3BCmd,{raw}"
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"}
        r = self.session.post(self._app_url(), data=data, headers=headers, timeout=20)
        r.raise_for_status()
        return r.text
