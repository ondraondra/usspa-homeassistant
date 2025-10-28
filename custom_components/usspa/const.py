
from __future__ import annotations

DOMAIN = "usspa"
DEFAULT_SCAN_INTERVAL = 30  # seconds

CONF_SERIAL = "serial"
CONF_PASSWORD = "password"
CONF_BASE_URL = "base_url"

DEFAULT_BASE_URL = "https://in.usspa.cz"

# Mapping for friendly names and metadata
MAPPING = {
    "ActTemp": {"name": "Water Temperature", "device_class": "temperature", "unit": "°C", "platform": "sensor"},
    "ReqTemp": {"name": "Setpoint Temperature", "device_class": None, "unit": "°C", "platform": "number"},
    "HeaterState": {"name": "Heater State", "platform": "binary_sensor"},
    "FiltrState": {"name": "Filtration State", "platform": "binary_sensor"},
    "Pump1": {"name": "Stream Speed", "platform": "select"},
    "Pump2": {"name": "Pump 2", "platform": "binary_sensor"},
    "Pump3": {"name": "Bubbles", "platform": "switch"},  # Switch remains for compatibility, light is separate for Light1 only
    "Light1": {"name": "Light 1", "platform": "light"},
    "Light2": {"name": "Light 2", "platform": "binary_sensor"},
    "LastConn": {"name": "Last Connection", "device_class": "timestamp", "platform": "sensor"},
    "ActDateTime": {"name": "Controller Time", "device_class": "timestamp", "platform": "sensor"},
    "ProductionDate": {"name": "Production Date", "device_class": "timestamp", "platform": "sensor"},
    "SpaInstallDate": {"name": "Install Date", "device_class": "timestamp", "platform": "sensor"},
    "EnergyResetDateTime": {"name": "Energy Reset Time", "device_class": "timestamp", "platform": "sensor"},
    "TmpEnergyResetDateTime": {"name": "Temp Energy Reset Time", "device_class": "timestamp", "platform": "sensor"},
    "HeatingSpeed": {"name": "Heating Speed", "platform": "sensor"},
    "Pump3ActSpeed": {"name": "Pump3 Actual Speed", "platform": "sensor"},
    "Pump3ReqSpeed": {"name": "Pump3 Requested Speed", "platform": "sensor"},
    "OzoneRuntime": {"name": "Ozone Runtime", "unit": "h", "platform": "sensor"},   # will convert seconds→hours
    "Pump3Runtime": {"name": "Pump3 Runtime", "unit": "h", "platform": "sensor"},   # will convert seconds→hours
    "OffMode": {"name": "Off Mode", "platform": "binary_sensor"},
    "SafeMode": {"name": "Heat blocking", "platform": "switch"},
    "Filtration": {"name": "Filtration Mode", "platform": "sensor"},
    "Model": {"name": "Model", "platform": "sensor"},
    "SwVer": {"name": "Software Version", "platform": "sensor"},
    "FanStart": {"name": "Fan Start Temperature", "device_class": "temperature", "unit": "°C", "platform": "sensor"},
    "FanStop": {"name": "Fan Stop Temperature", "device_class": "temperature", "unit": "°C", "platform": "sensor"},
}
