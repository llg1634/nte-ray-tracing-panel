# 异环光追解锁面板 / NTE Ray Tracing Panel vX.Y.Z

异环光线追踪 / 全景光追本地 WebUI。通过 OptiScaler DXGI/Streamline GPU spoof，让 `HTGame.exe` 看到所选目标显卡，从而解锁游戏内光追选项。

推荐发布标题：

```text
异环光追解锁面板：异环光线追踪 / 全景光追一键解锁工具 vX.Y.Z
```

搜索关键词：

```text
异环光追解锁，异环光线追踪开启，异环全景光追开启，异环光追选项不显示，异环光追灰色，异环 RTX 5060 开光追，异环 RTX 4060 开光追，异环显卡伪装，异环不改注册表光追，异环 winmm.dll 光追，异环 OptiScaler，NTE ray tracing unlock，NTE ray tracing option missing，NTE GPU spoof，Neverness To Everness ray tracing unlock，Ananta ray tracing unlock，RTX 4090 spoof，RTX 5080M spoof
```

## Highlights

- 本机 WebUI：`http://127.0.0.1:22642`
- 自动检测异环 `HTGame.exe`
- 一键准备 OptiScaler
- 一键备份并安装所选目标显卡 spoof
- 三档目标显卡：本机原配置、RTX 4090、RTX 5080M
- Manifest 备份恢复
- 深色/浅色 Mac 设置风界面

## Important

- 关闭浏览器标签页不会退出工具。
- 退出时请点击页面里的“退出工具”，或在任务管理器结束 `NTERayTracingPanel.exe`。
- 默认 DXGI 模式不修改系统显卡注册表。
- 不使用 ProcMon。

## Core Projects

```text
OptiScaler:
https://github.com/optiscaler/OptiScaler

DLSSTweaks:
https://github.com/emoose/DLSSTweaks
```

本项目解决的是异环光线追踪 / 全景光追解锁，核心是 OptiScaler DXGI/Streamline GPU spoof。DLSSTweaks 仅作为相关工具和旧本地文件兼容备份说明；本项目不实现 DLSS 低渲染比例流程。

## Files

- `NTERayTracingPanel.exe`
- `run_exe_as_admin.bat`
- `README.md`
- `README.en.md`
- `docs\`
