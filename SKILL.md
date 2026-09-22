---
name: lg-monitor-control
description: Safely diagnose and tune LG UltraGear/OLED monitors on Linux with DDC/CI, Hyprland, and Omarchy.
---

# LG monitor control

Use this procedure for LG UltraGear/OLED display diagnosis and tuning on Linux/Omarchy.
## Agent and platform adapters

This skill uses the interoperable `SKILL.md` format. Install it under `~/.agents/skills/lg-monitor-control/` for a shared default, or use the client-specific paths in `docs/agents.md`.

The control procedure is platform-adapted:

- Linux: `ddcutil`, DRM inspection, and the desktop compositor's monitor command.
- Hyprland/Omarchy: `ddcutil`, `hyprctl`, `modetest`, and `~/.config/hypr/monitors.lua`.
- macOS: MonitorControl, BetterDisplay, DisplayBuddy, or `ddcctl`; no native `ddcutil`.
- Windows: Monitorian, Twinkle Tray, ControlMyMonitor, `winddcutil`, or LG OnScreen Control.
- WSL: run DDC/monitor commands on the Windows host unless the host explicitly passes the display device through.

Keep the evidence model identical on every OS: discover the external display, snapshot current values, write one known control, read it back, and verify the active mode/bpc/VRR in the host display stack.


## Safety and scope

- Prefer DDC/CI over the monitor's DisplayPort/HDMI I²C channel. It is the supported, observable control path.
- Never send random bytes to `/dev/ttyACM*` or `/dev/hidraw*`. LG USB composite devices expose HID and CDC interfaces, but the USB protocol is proprietary and may include firmware/diagnostic commands.
- Never edit `/usr/share/omarchy/`; put Hyprland overrides in `~/.config/hypr/monitors.lua`.
- Snapshot state before changes: `ddcutil --display N dumpvcp /tmp/lg-monitor-before.vcp`.

## Identify and inspect

```bash
ddcutil detect
ddcutil --display 1 capabilities
ddcutil --display 1 getvcp 10 12 14 16 18 1A 87
ddcutil --display 1 getvcp f9 --show-unsupported
hyprctl monitors all
hyprctl configerrors
modetest -M amdgpu -c
```

Use the actual display number reported by `ddcutil detect`. Treat EDID model names as hints; product IDs can be shared by regional/firmware variants.

## Standard controls

- `0x10`: brightness.
- `0x12`: contrast.
- `0x14`: color preset; LG displays commonly expose `0x05` as 6500 K.
- `0x16`, `0x18`, `0x1A`: red, green, blue gain.
- `0x87`: sharpness.
- `0xF9`: LG UltraGear Black Stabilizer on models that return a valid range; neutral baseline is usually 50.

Only write a vendor-specific code after reading it and confirming a sane current/max range. Verify every write with `getvcp`; save with `ddcutil scs` only after verification.

Avoid blindly writing `0xF7` (often response time), `0xF8` (often FreeSync/Adaptive-Sync), `0x15` (picture mode), or side-channel addresses. Mappings vary by model and firmware.

## Recommended baseline

For accurate SDR:

- monitor color preset: 6500 K or sRGB mode when available;
- contrast 70/default;
- RGB 50/50/50 unless a colorimeter provides per-panel gains;
- sharpness 50;
- Black Stabilizer 50;
- HDR off for the SDR desktop;
- OLED Care/Screen Move/Screen Saver on.

Brightness is room-dependent. Apply the user's requested level, but note that high OLED brightness increases ABL and eye strain.

## Hyprland/Omarchy monitor profile

Use a description match when connector names can renumber:

```lua
local external = "desc:LG Electronics LG ULTRAGEAR+"
hl.monitor({
  output = external,
  mode = "2560x1440@239.97",
  position = "0x0",
  scale = 1.6,
  bitdepth = 10,
  cm = "srgb",
  vrr = 0,
})
```

- 240 Hz + 10 bpc + VRR off is the stable gaming profile when OLED VRR flicker is visible.
- 144 Hz + 10 bpc + VRR off is the lower-bandwidth fallback.
- VRR flicker is a known OLED behavior; fixed refresh is preferable when the user reports pulsing/flicker.
- An EDID can advertise 12 bpc while the active DRM connector only exposes 8..10 bpc. Inspect `modetest`; do not claim 12-bit if Hyprland reports `XRGB2101010` or the connector max is 10.
- After every Lua change: `hyprctl reload`, then `hyprctl configerrors`, then `hyprctl monitors all`.

## USB interfaces

LG UltraGear USB may expose `LG Monitor Controls` with HID and CDC ACM interfaces. This is useful for firmware/vendor software, not a documented universal OSD API. Use DDC/CI first. If a USB probe fails due permissions or a tool crash, report it and do not compensate with arbitrary HID/serial writes.

## Verification

```bash
ddcutil --display 1 getvcp 10 12 14 87 f9 --show-unsupported
hyprctl monitors all
hyprctl configerrors
cat /sys/class/drm/card*-DP-*/status
```

Evidence must distinguish configured intent from active output: `mode`, `vrr`, `currentFormat`, and DDC readback are the source of truth.
