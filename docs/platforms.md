# Operating systems, transports, and limits

The skill format is cross-platform. The **monitor control commands** are not identical across operating systems.

## OS matrix

| OS | Agent skill | Monitor control adapter | Status |
| --- | --- | --- | --- |
| **Linux** | Full | `ddcutil`, `modetest`, compositor tools | First-class; tested path |
| **Linux + Hyprland/Omarchy** | Full | `ddcutil` + `hyprctl` + `modetest` | Reference workflow |
| **Linux + KDE/GNOME/X11/other Wayland** | Full | `ddcutil` + the desktop's display tool | DDC works; compositor examples differ |
| **macOS** | Full guidance | MonitorControl, BetterDisplay, DisplayBuddy, or `ddcctl` | Adapter required; no native ddcutil |
| **Windows** | Full guidance | Monitorian, Twinkle Tray, ControlMyMonitor, winddcutil, or LG OnScreen Control | Adapter required; no native official ddcutil |
| **Windows + WSL** | Agent skill only by default | Run monitor commands on Windows host | WSL does not automatically expose host DDC/I²C |
| **BSD/other Unix** | Skill text | OS-specific DDC utility | Untested; contribute an adapter |

The skill never pretends a Linux command works on macOS or Windows. Use the same evidence model—read, write one setting, read back—but substitute the platform's monitor tool.

## Hardware and transport matrix

| Connection | Usually works | Common limitation |
| --- | --- | --- |
| Direct DisplayPort | Best for high refresh and bpc | Cable/driver still controls negotiated limits |
| Direct HDMI | Often supports DDC/CI | High refresh, RGB range, and bpc vary by HDMI version |
| USB-C DisplayPort Alt Mode | Often works | Dock firmware and bandwidth can cap bpc/refresh |
| Dock/KVM/adapter | Sometimes | DDC blocked, connector renamed, DSC/bpc limited, VRR unstable |
| Internal eDP panel | Usually no DDC/CI | Use OS brightness/GPU controls, not this skill's OSD workflow |

## Linux adapter

```bash
sudo apt install ddcutil edid-decode
# Arch-based distributions:
sudo pacman -S ddcutil edid-decode

ddcutil detect
ddcutil --display 1 capabilities
ddcutil --display 1 getvcp 10
```

For Hyprland/Omarchy:

```bash
hyprctl monitors all
hyprctl configerrors
modetest -M amdgpu -c
```

The GPU module may not be `amdgpu`; use the DRM tool appropriate to the host GPU.

## macOS adapter

Use a DDC-capable tool such as MonitorControl, BetterDisplay, DisplayBuddy, or `ddcctl`. The skill's VCP map remains useful, but commands and permissions are tool-specific. Confirm the tool's current syntax before writing values.

## Windows adapter

Use Monitorian, Twinkle Tray, ControlMyMonitor, `winddcutil`, or LG OnScreen Control. Prefer a tool that can read the current value after writing it. Keep the same invariants:

1. identify the correct external display;
2. snapshot or record current values;
3. write one known control;
4. read back;
5. verify refresh, bpc, VRR, and link state in the OS display settings.

## Universal limits

- DDC/CI must be enabled by the monitor and survive the physical path.
- A dock or KVM can hide DDC/CI and lower the negotiated bpc.
- EDID capabilities are advertisements; DRM/display settings report the active link.
- 12 bpc is not guaranteed just because EDID advertises it.
- OLED VRR flicker can remain even with a perfect link; fixed refresh is the mitigation.
- Exact D65/6500 K requires a colorimeter; a preset is a repeatable baseline, not a measurement.
- The LG USB HID/CDC protocol is proprietary; do not send random reports.
