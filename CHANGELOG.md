# 更新日志

## 0.1.6

- 新增目标显卡 profile 选择：本机原配置、RTX 4090、RTX 5080M。
- 后端统一下发 `profiles`，安装接口支持 `profile` 参数，并把所选 profile 写入 manifest。
- WebUI 重构安装区：目标显卡选择、DXGI/Full 模式和备份安装按统一逻辑展示。
- 更新本地构建与发布材料，便于 GitHub Release 分发。

## 0.1.5

- 纠正发布归属：移除旧 DLSS 面板项目引用，改为明确致谢 OptiScaler 和 DLSSTweaks。
- 强化边界说明：OptiScaler 是实际 GPU spoof 核心，DLSSTweaks 仅作为相关项目和旧本地文件兼容备份说明。
- 同步更新 README、英文 README、NOTICE、WebUI 说明卡、发布指南、Release Notes 模板和 Release Checklist。

## 0.1.4

- 优化 WebUI 顶部区域：新增 01 到 05 功能路径概览，分别对应选择游戏、准备 OptiScaler、安装解锁、备份恢复、退出工具。
- 增强“WebUI 与后端工具不同”的提示：关闭浏览器标签页不会退出 `NTERayTracingPanel.exe`，需要点击“退出工具”或结束 exe。
- 调整状态圆环，只显示安装状态，不塞入额外说明，避免视觉干扰。
- 补齐发布准备内容：Release 检查清单、Release Notes 模板、英文 README、NOTICE、SECURITY、CONTRIBUTING、打包脚本。

## 0.1.3

- 强化中文项目名和搜索定位：异环光线追踪一键、异环全景光追解锁、NTE Ray Tracing Panel、OptiScaler RTX 4090 spoof。
- README 第一屏补充本机 WebUI 地址、局部修改范围、退出后端服务说明。
- 同步更新英文 README 和发布文档中的项目定位。

## 0.1.2

- 重写 README 第一屏，强调异环 / Neverness To Everness / Ananta、光线追踪 / 全景光追、RTX 4090 spoof、DXGI / Streamline spoof。
- 新增中英文搜索关键词段。
- 补充“关闭网页不等于退出 exe”的常见问题。

## 0.1.1

- 新增英文 README：`README.en.md`。
- 新增第三方归属说明：本项目不是 OptiScaler 本体，也不是 NVIDIA 官方工具。
- 强化 `--noconsole` 打包兼容：后端日志输出使用安全写法，避免无 stdout 时 HTTP 接口异常。

## 0.1.0

- 新建 `NTE Ray Tracing Panel`，定位为异环光线追踪 / 全景光追解锁面板。
- 使用本地 WebUI，默认监听 `127.0.0.1:22642`。
- 新增异环 `HTGame.exe` 路径检测，支持选择游戏根目录、`Win64` 目录或 `HTGame.exe`。
- 新增 OptiScaler 最新 Release 下载与解包。
- 新增 RTX 4090 DXGI/Streamline spoof 默认配置。
- 新增每次安装前 manifest 备份，支持恢复 `winmm.dll`、`OptiScaler.ini`、`OptiScaler\` 等文件。
- 新增状态检测：运行中的 NTE 进程、`PROCMON` 残留、当前 NVIDIA 显卡、游戏目录安装状态、日志摘要。
- 新增 Mac 设置风 WebUI，只保留浅色和深色主题。

## 0.1.1 计划

- 增加 OptiScaler 日志的更细粒度解释。
- 增加“DXGI 模式成功但选项仍未出现”的排查路径。
- 增加启动器热修复后的安装状态对比。

## 0.2.0 计划

- 暴露 Full 实验模式：Registry/User32/FakeNVAPI spoof。
- 增加多显卡目标 DeviceId 自动选择。
- 增加一键导出诊断包，便于远程排错。
