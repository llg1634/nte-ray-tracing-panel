# 异环光追解锁面板 / NTE Ray Tracing Panel vX.Y.Z

给玩家的一键开光追本地 WebUI：解决《异环》没有光追选项、光追打不开、RTX 5060/4060 开不了光追的问题。工具会自动准备 OptiScaler，安装本地 `winmm.dll` 代理、`OptiScaler.ini`、`OptiScaler\` 和 `OptiScaler.log`，通过 DXGI/Streamline GPU spoof 解锁游戏内光追选项。

推荐发布标题：

```text
异环光线追踪一键部署面板 vX.Y.Z
```

搜索关键词：

```text
异环怎么开光追，异环光追怎么开，异环全景光追怎么开，异环没有光追选项，异环光追选项不显示，异环光追打不开，异环光追开不了，异环 RTX 5060 怎么开光追，异环 RTX 4060 怎么开光追，异环光追一键开启，异环光追一键安装，异环开光追工具，异环光追补丁，NTE how to enable ray tracing，NTE no ray tracing option，NTE ray tracing fix，NTE one-click ray tracing unlock
```

## Highlights

- 本机 WebUI：`http://127.0.0.1:22642`
- 自动检测异环 `HTGame.exe`
- 一键准备 OptiScaler
- 内置 `py7zz` / `7zz` 解压 OptiScaler `.7z`，不再把 Windows `tar.exe` 当作主路径
- 一键部署本地 `winmm.dll` 代理、`OptiScaler.ini`、`OptiScaler\` 和 `OptiScaler.log`
- 与 DLSS Panel 共存：RT Panel 负责 `winmm.dll` / `OptiScaler`，DLSS Panel 负责 `nvngx.dll` / `DLSSTweaks`
- 一键备份并安装所选目标显卡 spoof
- 四档目标显卡：本机原配置、RTX 5090、RTX 4090、RTX 5080M，其中 RTX 5090 是默认推荐
- Manifest 备份恢复
- 深色/浅色 Mac 设置风界面

## Important

- 关闭浏览器标签页不会退出工具。
- 退出时请点击页面里的“退出工具”，或在任务管理器结束 `NTERayTracingPanel.exe`。
- 默认 DXGI 模式不修改系统显卡注册表。
- 不使用 ProcMon。
- RTX 5090 profile 是默认推荐：`SpoofedGPUName=NVIDIA GeForce RTX 5090`、`SpoofedDeviceId=0x2B85`、`DxgiVRAM=32`。
- RTX 4090 保留为已验证备用；RTX 5080M 仅保留作实验对照。
- 光追选项通常需要默认画质预设在“极致”或以上才会出现。
- 如果遇到 `tar.EXE: LZMA codec is unsupported`，这是 OptiScaler 官方 `.7z` 自动解压兼容问题，不是本项目 Release `.zip` / `.exe` 损坏；当前版本会先用随包解压器处理，并保留手动解压兜底说明。

## Core Projects

```text
OptiScaler:
https://github.com/optiscaler/OptiScaler

DLSSTweaks:
https://github.com/emoose/DLSSTweaks
```

本项目解决的是异环光线追踪 / 全景光追解锁，核心是 OptiScaler DXGI/Streamline GPU spoof。`nvngx.dll` / `DLSSTweaks` 归 DLSS Panel 管理；本项目不写入、删除或恢复 `nvngx.dll`、`dlsstweaks.ini`，也不实现 DLSS 低渲染比例流程。

## Files

- `NTERayTracingPanel.exe`
- `run_exe_as_admin.bat`
- `README.md`
- `README.en.md`
- `docs\`
