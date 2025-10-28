# Changelog

All notable changes to this project will be documented in this file.

---

## [0.7.5] - 2025-10-28
### ✅ Fixed
- Resolved critical integration crash during setup caused by invalid coordinator initialization
- Replaced deprecated `async_track_time_interval` usage with proper `DataUpdateCoordinator` configuration
- Ensured timestamps are properly converted to timezone-aware ISO format
- Coordinator login logic now stable and executed only once per runtime

### 🧩 Improved
- Retained central entity mapping system introduced in 0.7.3
- Finalized visibility defaults:  
  - 6 main entities enabled & visible  
  - Diagnostics enabled but hidden  
  - Unknown data disabled by default  
- Finalized new icons on key controls

### ⚠️ Notes
> This version replaces 0.7.3, which was broken.  
> If you installed 0.7.3, update to 0.7.5 immediately.

---

## [0.7.3] - 2025-10-28 *(Withdrawn)*
> ❌ **Broken release — do not use**  
> Version had an invalid DataUpdateCoordinator init and failed to load.

### Added (before withdrawal)
- Central mapping table for all entities (platform, device_class, unit, icon, enabled, visible)
- Introduction of “primary 6” visible entities:
  - Water Temperature  
  - Stream Speed  
  - Bubbles  
  - Heat Blocking  
  - Temperature Setpoint  
  - Light  
- Runtime auto-conversion from seconds → hours

---

## [0.7.1] - 2025-10-27
### 🚀 First Public Release
- Initial working USSPA Home Assistant integration
- Basic sensors, switches, select, number, and light entities exposed
- Manual YAML install supported
- Reverse-engineered API communication via `/app/` endpoint
