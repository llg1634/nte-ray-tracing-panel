# Release Checklist

## Before Build

- [ ] `APP_VERSION` matches `CHANGELOG.md`.
- [ ] Chinese release title is `异环光追解锁面板：异环光线追踪 / 全景光追一键解锁工具`.
- [ ] `README.md` first screen has Chinese search keywords.
- [ ] `README.en.md` has English search keywords.
- [ ] WebUI exposes local original, RTX 4090, and RTX 5080M profile choices.
- [ ] Docs mention WebUI and backend exe are separate processes.
- [ ] Docs mention closing browser tab does not close the exe.
- [ ] Docs mention the “Exit Tool” button.
- [ ] `NOTICE.md` mentions OptiScaler as the GPU spoofing payload source.
- [ ] `NOTICE.md` mentions DLSSTweaks only as a related project and legacy-file backup boundary.
- [ ] Default mode keeps `Registry=false` and `User32=false`.
- [ ] No ProcMon tooling is present.

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
- Selectable GPU profiles: local original, RTX 4090, RTX 5080M.
- Local-only WebUI.
- Manifest backup and restore.
- Browser tab close does not exit backend.
- Default mode does not modify GPU registry.
