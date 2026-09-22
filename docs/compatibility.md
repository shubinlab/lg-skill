# Compatibility and limits

This skill is a **Linux/Omarchy control procedure**, not a universal LG firmware client. Compatibility is determined by the monitor's exposed DDC/CI/MCCS capabilities and the negotiated GPU link.

## Support tiers

| Tier | Hardware | Status | Controls |
| --- | --- | --- | --- |
| A — verified reference | LG UltraGear+ OLED, QHD, 240 Hz, DP, EDID GSM product `23676` | Tested | 6500 K, brightness, contrast, RGB, sharpness, Black Stabilizer `0xF9`, 240 Hz/10 bpc/fixed refresh |
| B — compatible | LG UltraGear/OLED with responsive DDC/CI and MCCS | Expected | Standard `0x10`, `0x12`, `0x14`, `0x16`, `0x18`, `0x1A`, `0x87`; vendor controls only after validation |
| C — partial | LG display with basic DDC/CI only | Supported with limits | Brightness/contrast/color may work; model-specific OSD controls may not |
| D — outside scope | Internal panel, no DDC/CI, or proprietary-only path | Not supported | Use GPU/compositor controls or the vendor's supported application |

The reference EDID is consistent with the LG 27GS95QE-B family, but EDID product IDs are not a guaranteed retail-model identifier. Confirm the physical label before reusing vendor-specific values.

## Transport matrix

| Transport | Discovery | Safe control | Limits |
| --- | --- | --- | --- |
| DisplayPort/HDMI DDC/CI | `/dev/i2c-*`, `ddcutil detect` | Yes | Requires DDC/CI and permissions |
| DRM/Hyprland | `hyprctl monitors`, `modetest` | Mode, scale, bpc, VRR | Reports negotiated state, not every OSD setting |
| USB HID | `/dev/hidraw*` | Not by default | Proprietary reports; never fuzz |
| USB CDC ACM | `/dev/ttyACM*` | Not by default | Proprietary protocol; may include firmware/diagnostic commands |
| LG OnScreen Control | Vendor software | Vendor-dependent | Not a native Linux API; USB protocol is not documented here |

## Capability matrix

### Safe and portable

- Brightness (`0x10`).
- Contrast (`0x12`).
- Color preset (`0x14`) when the monitor advertises it.
- RGB gains (`0x16`, `0x18`, `0x1A`).
- Sharpness (`0x87`) when the monitor exposes it.
- DDC/CI snapshots and readback.
- Hyprland mode/scale/bitdepth/VRR configuration.

### Model-validated, not universal

- Black Stabilizer (`0xF9`).
- Response Time (`0xF7`).
- FreeSync/Adaptive-Sync (`0xF8`).
- Picture Mode (`0x15`).
- LG side-channel addresses.

The skill may read these codes, but must not write them without a sane range and model evidence. A code listed in a capability string can still be broken or misreported by firmware.

### Not promised

- Colorimeter-grade calibration.
- 12-bit output when the active connector reports `max bpc: 8..10`.
- Elimination of OLED VRR brightness pulsing while VRR is enabled.
- OLED Care/Screen Move controls through a universal Linux API.
- Firmware updates or raw USB control.
- Correct behavior through every dock, KVM, adapter, or cable.

## Decision table

| Observation | Recommended action |
| --- | --- |
| DDC responds and DRM reports 10 bpc | Use 240 Hz + 10 bpc; disable VRR if flicker is visible |
| DDC responds but DRM caps at 8 bpc | Use the highest stable mode; test a direct DP 1.4 path |
| EDID says 12 bpc but DRM caps at 10 | Report active 10-bit; do not force 12 |
| OLED flickers with VRR | Fixed refresh first; 144 Hz is the fallback |
| `F9` returns a sane 0–100 range | Black Stabilizer may be validated and set to 50 |
| `F7`, `F8`, or `0x15` returns opaque values | Read only; do not fuzz or guess |
| USB exposes HID/CDC only | Use DDC/CI; do not write raw reports |
