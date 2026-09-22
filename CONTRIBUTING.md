# Contributing

Thanks for improving the LG monitor control skill.

## Development loop

1. Reproduce the behavior on a real monitor when hardware is required.
2. Read current DDC/CI state before changing it.
3. Add only model-confirmed VCP mappings; never guess from a similarly named display.
4. Keep public evidence sanitized: remove serials, hostnames, absolute paths, raw journals, and credentials.
5. Run the repository validation:

   ```bash
   python tests/validate.py
   ```

6. Explain the observed output, not only the intended configuration.

## Pull requests

Include:

- affected monitor/model and firmware information when safe to share;
- exact commands and readback used;
- before/after active DRM state;
- whether the change was tested through a dock, direct DisplayPort, or HDMI;
- a note about reversibility.

Do not include private EDID serials or raw USB captures in a public pull request.
