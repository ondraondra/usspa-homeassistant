
from __future__ import annotations
from typing import Dict, Any, Optional
from homeassistant.helpers.entity import EntityCategory

DOMAIN = "usspa"
DEFAULT_BASE_URL = "https://in.usspa.cz"
DEFAULT_SCAN_INTERVAL = 30

# Master mapping with platform, device_class, unit, icon, defaults
MAPPING: Dict[str, Dict[str, Any]] = {
    # Primary 6 (visible & enabled)
    "ActTemp":   {"name": "Water Temperature",    "platform": "sensor",  "device_class": "temperature", "unit": "°C", "icon": None,                     "enabled_default": True,  "visible_default": True},
    "Pump1":     {"name": "Stream Speed",         "platform": "select",  "device_class": None,          "unit": None, "icon": "mdi:turbine",            "enabled_default": True,  "visible_default": True},
    "Pump3":     {"name": "Bubbles",              "platform": "switch",  "device_class": None,          "unit": None, "icon": "mdi:chart-bubble",       "enabled_default": True,  "visible_default": True},
    "SafeMode":  {"name": "Heat blocking",        "platform": "switch",  "device_class": None,          "unit": None, "icon": "mdi:thermometer-alert",  "enabled_default": True,  "visible_default": True},
    "ReqTemp":   {"name": "Temperature Setpoint", "platform": "number",  "device_class": None,          "unit": "°C", "icon": "mdi:thermometer-water",  "enabled_default": True,  "visible_default": True},
    "Light1":    {"name": "Light",                "platform": "light",   "device_class": None,          "unit": None, "icon": None,                     "enabled_default": True,  "visible_default": True},

    # Enabled but hidden (diagnostic)
    "HeaterState":         {"name": "Heater State",           "platform": "binary_sensor", "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "FiltrState":          {"name": "Filtration State",       "platform": "binary_sensor", "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "Pump2":               {"name": "Pump 2",                 "platform": "binary_sensor", "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "LastConn":            {"name": "Last Connection",        "platform": "sensor",        "device_class": "timestamp",  "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "ActDateTime":         {"name": "Controller Time",        "platform": "sensor",        "device_class": "timestamp",  "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "ProductionDate":      {"name": "Production Date",        "platform": "sensor",        "device_class": "timestamp",  "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "SpaInstallDate":      {"name": "Install Date",           "platform": "sensor",        "device_class": "timestamp",  "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "EnergyResetDateTime": {"name": "Energy Reset Time",      "platform": "sensor",        "device_class": "timestamp",  "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "TmpEnergyResetDateTime":{"name":"Temp Energy Reset Time","platform": "sensor",        "device_class": "timestamp",  "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "HeatingSpeed":        {"name": "Heating Speed",          "platform": "sensor",        "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "Pump3ActSpeed":       {"name": "Pump3 Actual Speed",     "platform": "sensor",        "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "Pump3ReqSpeed":       {"name": "Pump3 Requested Speed",  "platform": "sensor",        "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "OzoneRuntime":        {"name": "Ozone Runtime",          "platform": "sensor",        "device_class": None,         "unit": "h",  "icon": None, "enabled_default": True,  "visible_default": False},
    "Pump3Runtime":        {"name": "Pump3 Runtime",          "platform": "sensor",        "device_class": None,         "unit": "h",  "icon": None, "enabled_default": True,  "visible_default": False},
    "OffMode":             {"name": "Off Mode",               "platform": "binary_sensor", "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "Filtration":          {"name": "Filtration Mode",        "platform": "sensor",        "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "Model":               {"name": "Model",                  "platform": "sensor",        "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},
    "SwVer":               {"name": "Software Version",       "platform": "sensor",        "device_class": None,         "unit": None, "icon": None, "enabled_default": True,  "visible_default": False},

    # Disabled by default
    "Light2":              {"name": "Light 2",                "platform": "binary_sensor", "device_class": None,         "unit": None, "icon": None, "enabled_default": False, "visible_default": False},
    "FanStart":            {"name": "Fan Start Temperature",  "platform": "sensor",        "device_class": "temperature","unit": "°C", "icon": None, "enabled_default": False, "visible_default": False},
    "FanStop":             {"name": "Fan Stop Temperature",   "platform": "sensor",        "device_class": "temperature","unit": "°C", "icon": None, "enabled_default": False, "visible_default": False},
}

def get_meta(key: str) -> Dict[str, Any]:
    m = MAPPING.get(key, {})
    return {
        "name": m.get("name"),
        "platform": m.get("platform"),
        "device_class": m.get("device_class"),
        "unit": m.get("unit"),
        "icon": m.get("icon"),
        "enabled_default": bool(m.get("enabled_default", False)),
        "visible_default": bool(m.get("visible_default", False)),
    }

def category_for(key: str) -> Optional[EntityCategory]:
    meta = get_meta(key)
    return None if meta["visible_default"] else EntityCategory.DIAGNOSTIC
