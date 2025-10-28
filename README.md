# USSPA

> **Unofficial community integration.** This project is based on a **reverse‑engineered private API** of the USSPA iOS app. **Use at your own risk; no warranty** of any kind.

Home Assistant integration to monitor and control USSPA hot tubs via the cloud endpoint.

## Features
- Auto-discovers all CSV keys from the cloud; applies **friendly mapping** for common ones.
- **Device per spa** (assign an Area, see serial, model, firmware).
- **Controls**
  - `light` — Light 1 (and Light 2, disabled by default until confirmed)
  - `switch` — Bubbles (Pump3), **Heat blocking** (Safe Mode)
  - `select` — Stream speed (Pump1): **off / low / high**
  - `number` — Temperature setpoint (text input, 0.5 °C step)
  - `button` — **Enable / Disable Heat Blocking**
- **Timestamps** are timezone-aware (UTC).
- Any **unknown keys** are created as disabled-by-default entities to avoid clutter.
- **Options Flow** to set polling interval (default **30 s**).

## Install (HACS – Custom Repository)
1. In Home Assistant, open **HACS → Integrations → ⋮ → Custom repositories**.
2. Add this repo URL: `https://github.com/ondraondra/usspa-homeassistant` with category **Integration**.
3. Click **Explore & Download Repositories**, search **USSPA**, install.
4. Restart Home Assistant.
5. **Settings → Devices & Services → Add Integration → USSPA** and enter your serial, password, and friendly name.

## Minimum HA
- Home Assistant **2024.6.0** or newer.

## Privacy
- Credentials are stored in Home Assistant as config entries.
- No telemetry or analytics; only the USSPA cloud is contacted to perform actions and polling.

