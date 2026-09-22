<div align="center">

<img src="assets/hero-monitor.svg" alt="LG monitor control skill" width="920">

# LG Monitor Control Skill

**A safe, evidence-first playbook for LG UltraGear/OLED monitors on Linux, Hyprland, and Omarchy.**

[![Validate](https://github.com/shubinlab/lg-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/shubinlab/lg-skill/actions/workflows/validate.yml)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-SKILL.md-6d5dfc)](SKILL.md)
[![Linux](https://img.shields.io/badge/Linux-supported-1793d1?logo=linux&logoColor=white)](#quick-start)
[![License](https://img.shields.io/badge/license-MIT-2ea44f)](LICENSE)

</div>

> Tune the monitor you actually have. Read the negotiated signal, change one verified control, and prove the active result.

![Control flow](assets/control-flow.svg)

## Why this exists

LG gaming monitors expose a useful standard control plane through **DDC/CI**. Their USB composite device may additionally expose HID and CDC interfaces, but the USB protocol is proprietary and unsafe to probe blindly. This skill keeps the reliable path boring:

- discover the real monitor and active connector;
- snapshot before mutation;
- use standard VCP controls first;
- gate vendor-specific controls by readback and sane ranges;
- treat EDID claims and compositor intent as hypotheses until DRM reports the active format;
- use fixed refresh when OLED VRR flicker is visible.

## Quick start

```bash
# 1. Discover the DDC display number.
ddcutil detect

# 2. Read capabilities and current state. Replace 1 with the detected display.
ddcutil --display 1 capabilities
ddcutil --display 1 getvcp 10 12 14 16 18 1A 87
ddcutil --display 1 getvcp f9 --show-unsupported

# 3. Snapshot before changing anything.
ddcutil --display 1 dumpvcp /tmp/lg-monitor-before.vcp

# 4. Verify the compositor and DRM state.
hyprctl monitors all
hyprctl configerrors
modetest -M amdgpu -c
```

If the monitor is external and the user reports flicker, prefer this Omarchy/Hyprland baseline:

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

Then reload and prove it:

```bash
hyprctl reload
hyprctl configerrors
hyprctl monitors all
```

## Safe baseline

| Layer | Baseline | Why |
| --- | --- | --- |
| Resolution | Native panel mode | Avoid scaling blur |
| Refresh | 240 Hz fixed, or 144 Hz fallback | Maximum motion clarity without VRR flicker |
| Output depth | 10 bpc when DRM exposes it | Highest verified depth on many DP paths |
| Color | 6500 K / sRGB for SDR | Neutral white point and sane gamut |
| Contrast | Default, commonly 70 | Avoid crushed highlights |
| RGB gains | 50 / 50 / 50 unless metered | Per-panel calibration values do not transfer |
| Sharpness | 50 | Neutral processing |
| Black Stabilizer | 50 | Avoid lifted blacks and crushed shadows |
| HDR | Off for SDR desktop | Enable only for HDR content |
| OLED Care | Screen Move/Screen Saver on | Reduce static-image risk |

Brightness is room-dependent. A high requested value can be valid for a bright room, but it increases OLED ABL and eye strain; a colorimeter target is more meaningful than a copied percentage.

## Control map

| VCP | Control | Confidence |
| --- | --- | --- |
| `0x10` | Brightness | Standard MCCS |
| `0x12` | Contrast | Standard MCCS |
| `0x14` | Color preset; LG commonly exposes `0x05` as 6500 K | Verified on compatible LG firmware |
| `0x16`, `0x18`, `0x1A` | Red/green/blue gain | Standard MCCS |
| `0x87` | Sharpness | Standard on many LG displays |
| `0xF9` | Black Stabilizer | Verified on compatible UltraGear firmware |
| `0xF7` | Often Response Time | Do not write without model verification |
| `0xF8` | Often FreeSync/Adaptive-Sync | Do not write without model verification |
| `0x15` | Often Picture Mode | Values vary by model and firmware |

Write only after reading the current/max value. Verify every write, then persist with `ddcutil scs`.

## Signal truth, not marketing truth

An EDID can advertise 12 bpc while the current DRM connector only negotiates 8–10 bpc. The active output is the source of truth:

```bash
hyprctl monitors all
modetest -M amdgpu -c
```

If Hyprland reports `XRGB2101010`, the active compositor path is 10-bit. If the connector reports `max bpc: 8..10`, do not claim 12-bit without changing the physical link and rechecking.

![Evidence card](assets/evidence-card.svg)

## USB: useful, but not a universal OSD API

Some LG UltraGear displays enumerate as `LG Monitor Controls` with HID and CDC ACM interfaces. That can support vendor software and firmware workflows, but no universal public OSD protocol is defined for the raw USB endpoints.

**Do not** send random bytes to `/dev/ttyACM*` or `/dev/hidraw*`. Prefer DDC/CI. If a USB probe fails because of permissions or a tool crash, record the failure instead of guessing at firmware commands.

## Omarchy integration

- User overrides live in `~/.config/hypr/monitors.lua`.
- Never modify `/usr/share/omarchy/`.
- Use description matching when DP connector names renumber.
- After every Lua edit: `hyprctl reload`, `hyprctl configerrors`, `hyprctl monitors all`.
- `hyprsunset` should be identity during color evaluation; a night-light profile changes the perceived white point.

## Troubleshooting

### Flicker with VRR

OLED VRR flicker is commonly most visible in dark scenes and during frame-time changes. Test in this order:

1. Keep 240 Hz and set VRR off.
2. If flicker remains, use 144 Hz with 10 bpc and VRR off.
3. Try a direct DP 1.4 cable instead of a dock/adapter.
4. Recheck `link-status`, `currentFormat`, and kernel DRM messages.

### 12-bit is advertised but unavailable

Check the connector's negotiated `max bpc`. A dock, adapter, DSC path, or driver can cap the active output below the EDID claim. Do not force unsupported values.

### A vendor VCP code returns nonsense

Stop. Read it again, inspect the advertised range, and compare a model-specific mapping. Unknown `F7`, `F8`, `0x15`, side-channel, and firmware controls are not safe to fuzz.

## Install as an agent skill

Copy or link `SKILL.md` into the skill directory used by your agent. The managed version of this skill is intentionally concise and keeps the same safety invariants.

## Evidence and references

- [ddcutil documentation](https://www.ddcutil.com/)
- [LG UltraGear 27GS95QE support](https://www.lg.com/us/support/product/lg-27GS95QE-B.AUS)
- [LG UltraGear VCP reverse-engineering notes](https://github.com/ddccontrol/ddccontrol-db/issues/80)
- [LG monitor DDC/CI controls](https://github.com/tyvsmith/streamcontroller-lg-monitor-control)
- [LG Black Stabilizer documentation](https://www.lg.com/us/support/help-library/lg-monitor-how-to-use-the-black-stablizer-function--20153247885189)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Security-sensitive reports belong in [SECURITY.md](SECURITY.md), not a public issue.

## License

MIT. See [LICENSE](LICENSE).
