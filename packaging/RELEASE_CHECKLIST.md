# Release Checklist

## Before Build

- [ ] `APP_VERSION` matches `CHANGELOG.md`.
- [ ] Chinese release title is `异环光线追踪一键部署面板 v0.1.10`.
- [ ] `README.md` first screen has Chinese search keywords.
- [ ] `README.en.md` has English search keywords.
- [ ] WebUI exposes local original, RTX 5090, RTX 4090, and RTX 5080M profile choices, with RTX 5090 selected by default.
- [ ] Docs mention WebUI and backend exe are separate processes.
- [ ] Docs mention closing browser tab does not close the exe.
- [ ] Docs mention the “Exit Tool” button.
- [ ] `NOTICE.md` mentions OptiScaler as the GPU spoofing payload source.
- [ ] `NOTICE.md` mentions `nvngx.dll` / `DLSSTweaks` belong to the DLSS Panel and are not written, deleted, or restored by RT Panel.
- [ ] Docs mention RT Panel owns `winmm.dll` / `OptiScaler`, while DLSS Panel owns `nvngx.dll` / `DLSSTweaks`.
- [ ] Default mode keeps `Registry=false` and `User32=false`.
- [ ] No ProcMon tooling is present.
- [ ] OptiScaler `.7z` extraction uses bundled `py7zz` / `7zz` before falling back to `tar.exe`.

## Verification

```powershell
python -m py_compile app.py
node -e "new Function(require('fs').readFileSync('web/app.js','utf8'))"
python app.py --no-browser
```

Open:

```text
http://127.0.0.1:22642
```

Check:

- [ ] `/api/state` returns `ok=true`.
- [ ] The page loads.
- [ ] Path detection works.
- [ ] Backup list renders.
- [ ] “Exit Tool” shuts down the backend.

## Package

Recommended files:

- [ ] `NTERayTracingPanel.exe`
- [ ] `run_exe_as_admin.bat`
- [ ] `README.md`
- [ ] `README.en.md`
- [ ] `CHANGELOG.md`
- [ ] `NOTICE.md`
- [ ] `LICENSE`
- [ ] `docs\`

## Release Notes

Mention:

- NTE ray tracing unlock via OptiScaler DXGI spoof.
- Selectable GPU profiles: local original, RTX 5090, RTX 4090, RTX 5080M; RTX 5090 is the default recommendation.
- Local-only WebUI.
- Manifest backup and restore.
- Browser tab close does not exit backend.
- Default mode does not modify GPU registry.
- RTX 4090 is documented as a verified fallback and RTX 5080M is documented as experimental.
- Ray tracing option visibility depends on the in-game Ultra/Extreme or higher preset.
- OptiScaler `.7z` extraction no longer depends on Windows `tar.exe` as the primary path.
