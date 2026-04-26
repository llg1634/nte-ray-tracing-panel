# 工作原理

## 已验证链路

当前机器是 `NVIDIA GeForce RTX 5060 Laptop GPU`。使用 OptiScaler 的 DXGI spoof 后，《异环》内光线追踪选项可以打开。因此本项目把这个已验证链路做成面板，而不是继续走全局注册表改名。

## 目标显卡 Profile

安装时先选择目标显卡：

- 本机原配置：读取当前 NVIDIA 显卡名称和 DeviceId，适合回到本机识别。
- RTX 4090：`NVIDIA GeForce RTX 4090` / `0x2684`。
- RTX 5080M：`NVIDIA GeForce RTX 5080 Laptop GPU` / `0x2C59`。

## 默认 DXGI 模式

默认 DXGI 模式会生成如下关键配置，其中 `SpoofedGPUName`、`SpoofedDeviceId` 和 `DxgiVRAM` 由所选 profile 决定：

```ini
TargetProcessName=HTGame.exe
SpoofedGPUName=<所选 profile 名称>
SpoofedVendorId=0x10de
SpoofedDeviceId=<所选 profile DeviceId>
TargetVendorId=0x10de
TargetDeviceId=<自动检测到的本机 NVIDIA DeviceId>
StreamlineSpoofing=true
Dxgi=true
DxgiVRAM=<所选 profile VRAM 或 auto>
Registry=false
User32=false
UseFakenvapi=false
OptiDllPath=.\OptiScaler
CheckForUpdate=false
```

安装文件落点：

```text
Win64\
  winmm.dll               <- OptiScaler.dll 复制而来
  OptiScaler.ini          <- 本工具生成
  OptiScaler\
    *.dll / *.ini         <- OptiScaler 依赖
    D3D12_Optiscaler\
```

## Full 实验模式

Full 模式会额外开启：

```ini
Registry=true
User32=true
UseFakenvapi=true
NvapiPath=.\OptiScaler\fakenvapi.dll
```

这个模式用于 DXGI 模式失败后的实验。默认不推荐，因为它更接近多层 API spoof，兼容性和反作弊风险都更高。

## 和改显卡注册表的区别

全局改名通常修改：

```text
HKLM\SYSTEM\CurrentControlSet\Enum\PCI\...\DeviceDesc
HKLM\SYSTEM\CurrentControlSet\Enum\PCI\...\FriendlyName
```

这会影响整机。开发工具、监控、脚本、许可证探测都可能看到假显卡名。

本项目默认不写这些注册表项，只让游戏目录里的本地代理 DLL 在 `HTGame.exe` 中工作。

## 备份恢复

每次安装会创建：

```text
Win64\_nte_rt_backups\<timestamp>\manifest.json
Win64\_nte_rt_backups\<timestamp>\files\...
```

manifest 会记录每个文件/目录是否原本存在、备份路径、哈希和安装操作。恢复时只处理 manifest 中记录的项目。

## 相关项目边界

[OptiScaler](https://github.com/optiscaler/OptiScaler) 是本项目实际使用的 GPU spoof 核心。面板下载并准备 OptiScaler Release，再把 `OptiScaler.dll` 安装为《异环》Win64 目录内的本地 `winmm.dll` 代理。

[DLSSTweaks](https://github.com/emoose/DLSSTweaks) 是相关图形注入/包装项目。这个面板不使用它的 DLSS 比例配置逻辑，只在备份恢复列表里保护旧的 `dlsstweaks.ini`、`dlsstweaks.log`，防止之前的实验文件被静默覆盖。

## 失败回滚

如果游戏无法启动：

1. 打开面板。
2. 选择同一个 Win64 路径。
3. 在“备份恢复”里选择最新备份。
4. 勾选“自动关闭异环和启动器”。
5. 点击恢复。

如果面板也无法使用，可以手动进入最新备份目录，根据 `manifest.json` 把 `files` 下的内容复制回 Win64。
