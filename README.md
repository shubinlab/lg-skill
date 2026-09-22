# LG monitor control skill

Reusable Linux/Omarchy procedure for diagnosing and tuning LG UltraGear/OLED monitors.

## Covers

- DDC/CI discovery and verified VCP writes
- 6500 K, brightness, contrast, RGB, sharpness, and Black Stabilizer
- Hyprland 240 Hz/10-bit profiles
- OLED VRR-flicker mitigation
- EDID versus active DRM bit-depth validation
- Safe handling of proprietary LG HID/CDC USB interfaces

The procedure is in [`SKILL.md`](SKILL.md). It deliberately avoids undocumented HID/serial writes and unverified vendor VCP commands.

## Evidence basis

- [ddcutil](https://www.ddcutil.com/)
- [LG UltraGear 27GS95QE support](https://www.lg.com/us/support/product/lg-27GS95QE-B.AUS)
- [LG UltraGear VCP reverse-engineering notes](https://github.com/ddccontrol/ddccontrol-db/issues/80)
- [LG monitor DDC/CI controls](https://github.com/tyvsmith/streamcontroller-lg-monitor-control)
