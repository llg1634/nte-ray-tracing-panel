# NTE Ray Tracing Panel / 异环光追解锁面板

Search keywords: Neverness To Everness ray tracing unlock, NTE ray tracing panel, Ananta ray tracing unlock, NTE RTX 4090 spoof, NTE RTX 5080M spoof, NTE OptiScaler, NTE path tracing, NTE full ray tracing, 异环光追解锁, 异环全景光追, 异环 RTX 5060 开光追.

`NTE Ray Tracing Panel` is a local WebUI for the verified Neverness To Everness / Ananta ray tracing unlock workflow. It wraps OptiScaler GPU spoofing with path detection, selectable GPU profiles, install, manifest backup, restore, logs, and release-ready documentation.

Local URL:

```text
http://127.0.0.1:22642
```

This is not an online service. The browser page is only the WebUI; the Python process or packaged exe is the local backend that reads/writes files. Closing the browser tab does not stop the backend. Use the "Exit Tool" button in the panel, or end `NTERayTracingPanel.exe` from Task Manager.

## Docs

Recommended reading order:

1. `docs/01-快速使用.md`
2. `docs/02-原理与试错路径.md`
3. `docs/03-备份恢复与修改范围.md`
4. `docs/04-发布指南.md`
5. `docs/05-常见问题.md`

## What It Does

Some NTE test builds hide ray tracing options based on a GPU model allowlist. The verified workaround is to make `HTGame.exe` see a higher whitelisted NVIDIA GPU through OptiScaler DXGI / Streamline spoofing.

Selectable profiles:

```ini
Local original profile = detected NVIDIA GPU name and DeviceId
SpoofedGPUName=NVIDIA GeForce RTX 4090
SpoofedDeviceId=0x2684
SpoofedGPUName=NVIDIA GeForce RTX 5080 Laptop GPU
SpoofedDeviceId=0x2C59
TargetProcessName=HTGame.exe
SpoofedVendorId=0x10de
StreamlineSpoofing=true
Dxgi=true
Registry=false
User32=false
```

## Safety Boundary

- No ProcMon, Sysmon, kernel tracing, or driver monitor is used.
- Default mode does not edit the global GPU registry under `HKLM\SYSTEM\CurrentControlSet\Enum\PCI`.
- Default mode only manages local files inside the game `Win64` directory.
- Every install creates `_nte_rt_backups\<timestamp>\manifest.json`.
- Restore follows the manifest instead of blindly deleting files.

## Quick Use

1. Run `run.bat`, or run the packaged exe.
2. Select the NTE install directory, the `Win64` directory, or `HTGame.exe`.
3. Click "Download / Prepare OptiScaler".
4. Close NTE and the launcher.
5. Select the target GPU profile: local original, RTX 4090, or RTX 5080M.
6. Click "Backup and Install Ray Tracing Unlock".
7. Launch the game and check the ray tracing options.

## Core Projects and Thanks

- [OptiScaler](https://github.com/optiscaler/OptiScaler): the GPU spoofing payload used by this panel. The panel prepares OptiScaler from its official GitHub Release and installs `OptiScaler.dll` as a local `winmm.dll` proxy under the selected NTE `Win64` directory.
- [DLSSTweaks](https://github.com/emoose/DLSSTweaks): a related graphics injection/wrapper project. This panel does not implement the DLSSTweaks DLSS render-scale workflow; it only backs up possible legacy `dlsstweaks.ini` and `dlsstweaks.log` files so previous experiments are not overwritten silently.

This project is not OptiScaler, not a DLSSTweaks fork, and not an NVIDIA tool. It is a game-specific installer, backup, restore, and explanation WebUI around the verified OptiScaler workflow. See `NOTICE.md`.
