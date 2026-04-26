# 异环光追解锁面板：异环光线追踪 / 全景光追一键解锁工具

搜索关键词：异环光追解锁、异环光线追踪开启、异环全景光追开启、异环光追选项不显示、异环光追灰色、异环 RTX 5060 开光追、异环 RTX 4060 开光追、异环显卡伪装、异环不改注册表光追、异环 winmm.dll 光追、异环 HTGame.exe 光追、异环 OptiScaler、异环 RTX 4090 spoof、异环 RTX 5080M spoof、NTE Ray Tracing Panel、Neverness To Everness ray tracing unlock、NTE ray tracing option missing、Ananta ray tracing unlock、OptiScaler DXGI spoof。

`异环光追解锁面板 / NTE Ray Tracing Panel` 是用于解决《异环》光追选项不显示、光线追踪 / 全景光追无法开启的本地 WebUI 工具。它把当前已验证成功的 OptiScaler `winmm.dll + OptiScaler.ini` GPU spoof 流程做成可检测、可选择目标显卡、可备份、可恢复、可解释的一键工具。

English README: [README.en.md](README.en.md)

Local URL:

```text
http://127.0.0.1:22642
```

它不是在线服务，只在本机运行。本机网页负责显示、选择目录和发起操作；Python / exe 后端负责监听 `127.0.0.1:22642`、下载 OptiScaler、写入文件、备份和恢复。只关闭浏览器标签页不会退出后端服务，需要在面板里点击“退出工具”，或者在任务管理器里结束 `NTERayTracingPanel.exe`。

## 搜索关键词 / Search Keywords

异环光追解锁，异环光线追踪开启，异环全景光追开启，异环光追选项不显示，异环光追灰色，异环路径追踪，异环 RTX 5060 开光追，异环 RTX 4060 开光追，异环 4060 开光追，异环显卡伪装，异环不改注册表光追，异环注册表替代方案，异环 winmm.dll 光追，异环 HTGame.exe 光追，异环 OptiScaler，异环 DXGI spoof，异环 Streamline spoof，异环 RTX 4090 spoof，异环 RTX 5080M spoof。

Neverness To Everness ray tracing unlock, Neverness To Everness path tracing unlock, NTE ray tracing unlock, NTE ray tracing panel, NTE full ray tracing unlock, NTE path tracing unlock, NTE ray tracing option missing, NTE ray tracing not showing, NTE GPU spoof, NTE RTX 4090 spoof, NTE RTX 5080M spoof, NTE OptiScaler, NTE winmm.dll, NTE HTGame.exe, DXGI spoof, Streamline spoof, Ananta ray tracing unlock, Ananta path tracing unlock.

## 项目定位

这个项目的重点不是“通用 Mod 管理器”，而是把异环这个具体场景里的光追解锁路径做成可复用流程：

- 异环当前测试版本会按 GPU 型号白名单隐藏光线追踪选项。
- 当前机器已验证：通过 OptiScaler DXGI/Streamline spoof 成白名单目标后，游戏内光线追踪选项可打开。
- 直接改系统显卡注册表是整机级影响，不适合主力开发机。
- 本工具默认只写游戏 `Win64` 目录内的本地代理文件，并提供 manifest 备份恢复。

## 能解决什么

部分 RTX 50/40/30 系显卡实际支持光追，但《异环》测试版本会按显卡型号白名单隐藏“光线追踪 / 全景光追”选项。手动改 Windows 显卡注册表是整机级影响，不适合主力开发机。

本工具默认使用 OptiScaler 的 DXGI/Streamline GPU spoof，把 `HTGame.exe` 看到的 GPU 名称伪装为所选目标显卡，从而解锁游戏里的光追选项。当前 WebUI 提供三档：本机原配置、`NVIDIA GeForce RTX 4090`、`NVIDIA GeForce RTX 5080 Laptop GPU`。这个方法已经在当前机器上验证：安装后游戏内光线追踪选项可打开。

## 文档导航

第一次使用建议按顺序看：

1. [快速使用](docs/01-快速使用.md)
2. [原理与试错路径](docs/02-原理与试错路径.md)
3. [备份恢复与修改范围](docs/03-备份恢复与修改范围.md)
4. [发布指南](docs/04-发布指南.md)
5. [常见问题](docs/05-常见问题.md)

## 安全边界

- 不使用 ProcMon、Sysmon、驱动监控或内核抓取工具。
- 默认不修改 `HKLM\SYSTEM\CurrentControlSet\Enum\PCI` 显卡注册表。
- 默认只管理游戏目录内这些路径：
  - `winmm.dll`
  - `OptiScaler.ini`
  - `OptiScaler.log`
  - `OptiScaler\`
  - 旧方案兼容备份：`dlsstweaks.ini`、`dlsstweaks.log`
- 每次安装前都会创建 `_nte_rt_backups\<timestamp>\manifest.json`。
- 恢复时严格按 manifest 操作，避免误删非本工具文件。

## 使用

1. 运行 `run.bat`，或双击发布版 `NTERayTracingPanel.exe`。
2. 页面打开后选择《异环》安装根目录，或直接选择 `Client\WindowsNoEditor\HT\Binaries\Win64`。
3. 点击“下载/准备 OptiScaler”。
4. 选择目标显卡 profile：本机原配置、RTX 4090 或 RTX 5080M。
5. 确认游戏和启动器已关闭。
6. 点击“备份并安装光追解锁”。
7. 启动游戏，在画质设置里检查光线追踪选项。

## 运行与退出

这个工具分成两层：

- 前端 WebUI：浏览器里的页面，只负责显示状态和发起操作。
- 后端服务：`NTERayTracingPanel.exe` 或 `python app.py`，负责监听端口、选择文件夹、写入文件、备份恢复。

所以只关闭网页标签页不会关闭后端服务，`22642` 端口也会继续被占用。需要退出时，在 WebUI 底部点击“退出工具”。如果页面已经关掉，可以重新打开：

```text
http://127.0.0.1:22642
```

然后再点击“退出工具”；或者在任务管理器里结束 `NTERayTracingPanel.exe`。

## 恢复

在页面的“备份与恢复”卡片里选择最近备份，点击恢复。

也可以用命令行恢复：

```powershell
python app.py --no-browser
```

然后在 WebUI 里恢复指定备份。

## 原理

OptiScaler 的 GPU spoof 能改写游戏进程通过 DXGI/Streamline 读取到的显卡描述、VendorId、DeviceId 和显存信息。本工具会按 WebUI 选择生成配置。三档目标显卡：

- 本机原配置：读取当前 NVIDIA 显卡名称和 DeviceId，适合回到本机识别。
- RTX 4090：`SpoofedGPUName=NVIDIA GeForce RTX 4090`，`SpoofedDeviceId=0x2684`。
- RTX 5080M：`SpoofedGPUName=NVIDIA GeForce RTX 5080 Laptop GPU`，`SpoofedDeviceId=0x2C59`。

所有 profile 都会保留这些默认边界：

- `TargetProcessName=HTGame.exe`
- `SpoofedVendorId=0x10de`
- `Dxgi=true`
- `StreamlineSpoofing=true`
- `Registry=false`
- `User32=false`

这和全局注册表改名不同：注册表改名会影响整机，DXGI spoof 只在本地代理 DLL 被 `HTGame.exe` 加载后生效。

## 版本路线

见 `CHANGELOG.md`。

## 核心项目与致谢

- [OptiScaler](https://github.com/optiscaler/OptiScaler)：本项目的 GPU spoof 核心来源。面板会从 OptiScaler 官方 GitHub Release 准备 `OptiScaler.dll`，并把它安装为《异环》Win64 目录内的本地 `winmm.dll` 代理。
- [DLSSTweaks](https://github.com/emoose/DLSSTweaks)：相关图形注入/包装工具。本项目不使用 DLSSTweaks 的 DLSS 比例配置流程，只在备份恢复时识别你之前可能留下的 `dlsstweaks.ini`、`dlsstweaks.log`，避免覆盖旧实验文件。

本项目不是 OptiScaler 本体、不是 DLSSTweaks 分支，也不是 NVIDIA 官方工具；它只是围绕 OptiScaler 的《异环》专用安装、备份、恢复和说明面板。
