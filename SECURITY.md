# Security policy

## Scope

This project documents monitor configuration. It is not a firmware flasher and does not define the proprietary LG USB protocol.

## Safe behavior

- Prefer DDC/CI read/write operations with verified VCP ranges.
- Snapshot settings before mutation.
- Never fuzz HID or CDC ACM endpoints.
- Never publish credentials, USB captures containing host data, monitor serials, EDIDs with identifying fields, or raw system logs.

## Reporting

For a suspected unsafe command or documentation error, open a private GitHub security report when available. If private reporting is unavailable, contact the maintainer before publishing exploit details.

## Do not publish

Do not publish passwords, access tokens, private USB traces, complete EDIDs with serial numbers, hostnames, absolute home paths, or unredacted diagnostic archives.
