
# USSPA (Unofficial) — Home Assistant Custom Integration

- Config Flow (UI): asks for **serial** and **password**.
- Polls the USSPA cloud and parses the semicolon-separated `name,value,upDate` triplets.
- **All discovered keys** become entities:
  - Known keys use friendly names/units (see `MAPPING` in `const.py`) and are **enabled by default**.
  - Unknown keys are created **disabled by default** (hidden) — you can enable from the Entity Registry.
- Adds a switch for **Light1** (on/off via `SetLight1;Light1,1/0`).
- Service `usspa.send_command` to send arbitrary raw commands.

## Install
1. Copy `custom_components/usspa/` to your Home Assistant `config/custom_components/`.
2. Restart Home Assistant.
3. Settings → Devices & Services → Add Integration → search **USSPA**.
4. Enter serial (e.g., `LRN18040`) and password.

## Notes
- This is unofficial and replicates the web client cookie+login flow.
- If your controller exposes additional keys, they will appear as disabled sensors automatically; enable the ones you want.


## Controls added
- **Switch**: Light 1 (on/off) → `SetLight1;Light1,1/0`
- **Switch**: Bubbles (Pump3) (on/off) → `SetPump3;Pump3,1/0`
- **Fan**: Stream (Pump1) with presets `off/low/high` → `SetPump1;Pump1,0/1/2`
- **Number**: Temperature setpoint (ReqTemp) → `SetReqTemp;ReqTemp,<value>`


## Upgrades
- **Light entity** for Light 1 (on/off).
- **Runtime auto-conversion**: any `*Runtime` value parsed as seconds is exposed in **hours** (unit `h`).
- **Better device classes & units**:
  - Temperature sensors show `°C`.
  - Timestamps (`LastConn`, `ActDateTime`, dates) exposed as `timestamp` device class.
  - `FanStart` / `FanStop` treated as temperatures in `°C`.
