# Notice

`NTE Ray Tracing Panel` is an independent local WebUI and automation wrapper for Neverness To Everness / Ananta.

## OptiScaler

The GPU spoofing payload is provided by OptiScaler:

```text
https://github.com/optiscaler/OptiScaler
```

The panel downloads OptiScaler from the official GitHub Release endpoint at runtime, unless a release has already been prepared under `tools/optiscaler`.

This project is not OptiScaler, not an NVIDIA tool, and not a general mod manager. Keep OptiScaler's license files when redistributing a packaged build that includes OptiScaler binaries.

## DLSSTweaks

```text
https://github.com/emoose/DLSSTweaks
```

DLSSTweaks is a related graphics injection/wrapper project. `NTE Ray Tracing Panel` does not copy or implement its DLSS render-scale workflow. `nvngx.dll` / `DLSSTweaks` belong to the DLSS Panel; this panel only reports compatibility when `nvngx.dll` + `dlsstweaks.ini` are present and never writes, deletes, or restores those files.

## Scope

The default install mode writes only local files under the selected game's `Win64` directory. It does not globally rename the system GPU.
