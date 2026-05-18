from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
import winreg
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


APP_VERSION = "0.1.10"
APP_CN_NAME = "异环光追解锁面板"
APP_FULL_CN_NAME = "异环光线追踪 / 全景光追一键解锁工具"
APP_EN_NAME = "NTE Ray Tracing Panel"
APP_SEARCH_KEYWORDS = [
    "异环怎么开光追",
    "异环光追怎么开",
    "异环全景光追怎么开",
    "异环没有光追选项",
    "异环光追打不开",
    "异环光追开不了",
    "异环光追解锁",
    "异环光追一键开启",
    "异环光追一键部署",
    "异环光追一键安装",
    "异环开光追工具",
    "异环光追工具",
    "异环光追补丁",
    "异环光线追踪怎么开",
    "异环光线追踪开启",
    "异环全景光追",
    "异环全景光追开启",
    "异环光追开启",
    "异环光追选项不显示",
    "异环光追灰色",
    "异环 5060 没有光追",
    "异环 4060 没有光追",
    "异环 RTX 5060 怎么开光追",
    "异环 RTX 4060 怎么开光追",
    "异环 RTX 5060 开光追",
    "异环 RTX 4060 开光追",
    "异环显卡伪装",
    "异环 不改注册表 光追",
    "异环 winmm.dll 光追",
    "异环 winmm.dll 一键安装",
    "异环 HTGame.exe 光追",
    "异环 OptiScaler",
    "异环 OptiScaler 一键安装",
    "异环 RTX 5090 spoof",
    "异环 RTX 4090 spoof",
    "异环 RTX 5080M spoof",
    "NTE how to enable ray tracing",
    "how to enable ray tracing in NTE",
    "NTE no ray tracing option",
    "NTE ray tracing fix",
    "NTE ray tracing tool",
    "NTE one-click ray tracing unlock",
    "NTE one-click OptiScaler install",
    "NTE ray tracing unlock",
    "Neverness To Everness ray tracing",
    "Neverness To Everness ray tracing unlock",
    "Neverness To Everness how to enable ray tracing",
    "Neverness To Everness no ray tracing option",
    "NTE ray tracing option missing",
    "NTE ray tracing not showing",
    "NTE GPU spoof",
    "NTE OptiScaler DXGI spoof",
    "Ananta how to enable ray tracing",
    "Ananta no ray tracing option",
    "Ananta path tracing",
    "Ananta ray tracing unlock",
]
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 22642
GITHUB_RELEASE_API = "https://api.github.com/repos/optiscaler/OptiScaler/releases/latest"
GAME_EXE = "HTGame.exe"

RUN_DIR = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
RESOURCE_DIR = Path(getattr(sys, "_MEIPASS", RUN_DIR))
WEB_DIR = RESOURCE_DIR / "web"
TOOLS_DIR = RUN_DIR / "tools" / "optiscaler"

MANIFEST_OWNER = "nte-ray-tracing-panel"
RUNTIME_LAYOUT = "rt-optiscaler-winmm-v2"

MANAGED_FILES = (
    "winmm.dll",
    "OptiScaler.ini",
    "OptiScaler.log",
)
MANAGED_DIRS = ("OptiScaler",)
CANONICAL_MANAGED_RELS = {name.lower() for name in (*MANAGED_FILES, *MANAGED_DIRS)}
DLSS_PANEL_RELS = {"nvngx.dll", "dlsstweaks.ini", "dlsstweaks.log"}
BACKUP_DIR_NAME = "_nte_rt_backups"

FALLBACK_LOCAL_PROFILE = {
    "id": "local",
    "label": "本机原配置",
    "gpuName": "NVIDIA GeForce RTX 5060 Laptop GPU",
    "vendorId": "0x10de",
    "deviceId": "0x2d19",
    "vramGb": "auto",
    "description": "使用当前机器检测到的 NVIDIA 显卡名称和 DeviceId，适合回到本机识别。",
}

STATIC_PROFILES = {
    "rtx5090": {
        "id": "rtx5090",
        "label": "RTX 5090",
        "gpuName": "NVIDIA GeForce RTX 5090",
        "vendorId": "0x10de",
        "deviceId": "0x2B85",
        "vramGb": "32",
        "description": "当前默认推荐目标，使用 32GB VRAM 的 RTX 5090 白名单配置。",
    },
    "rtx4090": {
        "id": "rtx4090",
        "label": "RTX 4090",
        "gpuName": "NVIDIA GeForce RTX 4090",
        "vendorId": "0x10de",
        "deviceId": "0x2684",
        "vramGb": "16",
        "description": "已验证可正常显示光线追踪选项的备用白名单目标。",
    },
    "rtx5080m": {
        "id": "rtx5080m",
        "label": "RTX 5080M",
        "gpuName": "NVIDIA GeForce RTX 5080 Laptop GPU",
        "vendorId": "0x10de",
        "deviceId": "0x2C59",
        "vramGb": "16",
        "description": "实验性目标，保留用于对照测试，不作为默认推荐。",
    },
}
DEFAULT_PROFILE_ID = "rtx5090"


class AppError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def safe_log(message: str, *, error: bool = False) -> None:
    stream = sys.stderr if error else sys.stdout
    if stream is None:
        return
    try:
        stream.write(message + "\n")
        stream.flush()
    except Exception:
        pass


def now_id() -> str:
    stamp = datetime.now()
    return stamp.strftime("%Y%m%d-%H%M%S") + f"-{stamp.microsecond // 1000:03d}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def normalize_rel(rel: str) -> str:
    return rel.replace("/", "\\").strip("\\").lower()


def rel_name(rel: str) -> str:
    return normalize_rel(rel).split("\\")[-1]


def is_dlss_panel_rel(rel: str) -> bool:
    return rel_name(rel) in DLSS_PANEL_RELS


def is_canonical_managed_rel(rel: str) -> bool:
    return normalize_rel(rel) in CANONICAL_MANAGED_RELS


def contains_bytes(path: Path, needle: bytes, *, limit: int | None = None) -> bool:
    if not path.is_file():
        return False
    remaining = limit
    with path.open("rb") as fh:
        while True:
            if remaining is not None and remaining <= 0:
                return False
            size = 1024 * 1024 if remaining is None else min(1024 * 1024, remaining)
            chunk = fh.read(size)
            if not chunk:
                return False
            if needle in chunk:
                return True
            if remaining is not None:
                remaining -= len(chunk)


def looks_like_optiscaler_proxy(path: Path) -> bool:
    try:
        return path.is_file() and path.stat().st_size > 1_000_000 and contains_bytes(path, b"OptiScaler")
    except OSError:
        return False


def looks_like_rt_optiscaler_ini(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return "OptiDllPath" in text and r".\OptiScaler" in text and "TargetProcessName=HTGame.exe" in text


def looks_like_optiscaler_dir(path: Path) -> bool:
    if not path.is_dir():
        return False
    return (path / "_source_OptiScaler.ini").is_file() or any(path.glob("*.dll"))


def looks_like_optiscaler_log(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.stat().st_size == 0:
        return True
    text = path.read_text(encoding="utf-8", errors="replace")
    return "OptiScaler" in text


def directory_fingerprint(path: Path) -> dict:
    digest = hashlib.sha256()
    count = 0
    for file in sorted((item for item in path.rglob("*") if item.is_file()), key=lambda item: str(item.relative_to(path)).lower()):
        rel = file.relative_to(path).as_posix().lower()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(sha256(file).encode("ascii"))
        digest.update(b"\0")
        count += 1
    return {"exists": True, "kind": "dir", "fileCount": count, "sha256": digest.hexdigest().upper()}


def item_fingerprint(path: Path) -> dict:
    if not path.exists():
        return {"exists": False}
    if path.is_dir():
        return directory_fingerprint(path)
    return {
        "exists": True,
        "kind": "file",
        "size": path.stat().st_size,
        "sha256": sha256(path),
    }


def fingerprint_matches(path: Path, expected: dict | None) -> bool:
    if not expected:
        return False
    current = item_fingerprint(path)
    if bool(current.get("exists")) != bool(expected.get("exists")):
        return False
    if not current.get("exists"):
        return True
    return current.get("kind") == expected.get("kind") and current.get("sha256") == expected.get("sha256")


def ensure_under(path: Path, base: Path) -> Path:
    resolved = path.resolve()
    root = base.resolve()
    if resolved != root and root not in resolved.parents:
        raise AppError(f"拒绝操作工作目录外路径: {resolved}", 500)
    return resolved


def run_command(args: list[str], *, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def run_powershell(script: str, *, timeout: int = 15) -> str:
    proc = run_command(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise AppError(proc.stderr.strip() or "PowerShell 命令执行失败。", 500)
    return proc.stdout.strip()


def running_processes() -> list[dict]:
    try:
        text = run_powershell(
            "Get-Process HTGame,NTEGame,NTEBrowser,NTEWebBooster -ErrorAction SilentlyContinue | "
            "Select-Object ProcessName,Id,Path | ConvertTo-Json -Compress",
            timeout=8,
        )
    except Exception:
        return []
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        data = [data]
    return data if isinstance(data, list) else []


def close_game_processes() -> list[dict]:
    before = running_processes()
    if not before:
        return []
    run_powershell(
        "Get-Process HTGame,NTEGame,NTEBrowser,NTEWebBooster -ErrorAction SilentlyContinue | Stop-Process -Force",
        timeout=15,
    )
    time.sleep(1.5)
    return before


def procmon_filter_state() -> dict:
    try:
        proc = run_command(["fltmc", "filters"], timeout=6)
    except Exception as exc:
        return {"available": False, "present": False, "message": str(exc)}
    text = (proc.stdout or "") + (proc.stderr or "")
    present = "PROCMON" in text.upper()
    return {
        "available": proc.returncode == 0,
        "present": present,
        "message": "检测到 PROCMON 过滤驱动，建议重启后再启动游戏。" if present else "未检测到 PROCMON 过滤驱动。",
    }


def get_nvidia_adapters() -> list[dict]:
    try:
        text = run_powershell(
            "Get-CimInstance Win32_VideoController | "
            "Select-Object Name,PNPDeviceID,DriverVersion,AdapterRAM,VideoProcessor | ConvertTo-Json -Compress",
            timeout=10,
        )
    except Exception:
        return []
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if isinstance(data, dict):
        data = [data]
    rows = []
    for item in data:
        pnp = item.get("PNPDeviceID") or ""
        if "VEN_10DE" not in pnp.upper() and "NVIDIA" not in (item.get("Name") or "").upper():
            continue
        device_match = re.search(r"DEV_([0-9A-Fa-f]{4})", pnp)
        device_id = f"0x{device_match.group(1).lower()}" if device_match else None
        item["DeviceIdHex"] = device_id
        item["Registry"] = read_device_registry(pnp)
        rows.append(item)
    return rows


def local_profile_from_adapter(adapters: list[dict] | None = None) -> dict:
    profile = dict(FALLBACK_LOCAL_PROFILE)
    adapter = adapters[0] if adapters else None
    if adapter:
        profile["gpuName"] = adapter.get("Name") or profile["gpuName"]
        profile["deviceId"] = adapter.get("DeviceIdHex") or profile["deviceId"]
        profile["description"] = f"当前检测到的本机显卡：{profile['gpuName']} / {profile['deviceId']}。"
    return profile


def spoof_profiles(adapters: list[dict] | None = None) -> list[dict]:
    return [
        local_profile_from_adapter(adapters),
        dict(STATIC_PROFILES["rtx5090"]),
        dict(STATIC_PROFILES["rtx4090"]),
        dict(STATIC_PROFILES["rtx5080m"]),
    ]


def resolve_profile(profile_id: str | None, adapters: list[dict] | None = None) -> dict:
    selected = (profile_id or DEFAULT_PROFILE_ID).strip().lower()
    if selected == "local":
        return local_profile_from_adapter(adapters)
    if selected in STATIC_PROFILES:
        return dict(STATIC_PROFILES[selected])
    raise AppError("目标显卡配置无效。")


def read_device_registry(pnp_device_id: str) -> dict:
    if not pnp_device_id:
        return {}
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"SYSTEM\CurrentControlSet\Enum\{pnp_device_id}") as key:
            result = {}
            for value in ("DeviceDesc", "FriendlyName"):
                try:
                    result[value], _ = winreg.QueryValueEx(key, value)
                except FileNotFoundError:
                    result[value] = None
            return result
    except OSError:
        return {}


def expand_user_path(value: str | None) -> Path:
    if not value or not value.strip():
        raise AppError("请选择或输入游戏路径。")
    cleaned = value.strip().strip('"')
    return Path(os.path.expandvars(cleaned)).expanduser()


def likely_game_paths(base: Path) -> list[Path]:
    return [
        base / GAME_EXE,
        base / "Client" / "WindowsNoEditor" / "HT" / "Binaries" / "Win64" / GAME_EXE,
        base / "WindowsNoEditor" / "HT" / "Binaries" / "Win64" / GAME_EXE,
        base / "HT" / "Binaries" / "Win64" / GAME_EXE,
        base / "Binaries" / "Win64" / GAME_EXE,
    ]


def limited_find_game(base: Path, limit: int = 160000) -> Path | None:
    if not base.is_dir():
        return None
    skipped = {"$RECYCLE.BIN", "System Volume Information", "Saved", "Logs", "UserData", "cef_cache_0"}
    checked = 0
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in skipped and not d.startswith(".")]
        checked += len(files)
        if GAME_EXE in files:
            return Path(root) / GAME_EXE
        if checked > limit:
            break
    return None


def detect_game(path_value: str | None) -> dict:
    base = expand_user_path(path_value)
    if not base.exists():
        raise AppError("路径不存在。")
    exe: Path | None = None
    if base.is_file():
        if base.name.lower() != GAME_EXE.lower():
            raise AppError("请选择异环安装根目录、Win64 文件夹，或 HTGame.exe。")
        exe = base
    else:
        for candidate in likely_game_paths(base):
            if candidate.is_file():
                exe = candidate
                break
        if exe is None:
            exe = limited_find_game(base)
    if exe is None:
        raise AppError("没有找到 HTGame.exe。")
    win64 = exe.parent
    return {
        "input": str(base),
        "exe": str(exe),
        "win64": str(win64),
        "install": inspect_install(win64),
        "backups": list_backups(win64),
    }


def common_game_candidates() -> list[Path]:
    candidates = []
    if os.environ.get("NTE_GAME_PATH"):
        candidates.append(Path(os.environ["NTE_GAME_PATH"]))
    candidates.extend(Path(f"{drive}:\\Neverness To Everness") for drive in "CDEFGHIJKLMNOPQRSTUVWXYZ")
    return candidates


def detect_common_game() -> dict | None:
    for candidate in common_game_candidates():
        try:
            if candidate.exists():
                return detect_game(str(candidate))
        except Exception:
            continue
    return None


def run_folder_dialog() -> str | None:
    script = r"""
Add-Type -AssemblyName System.Windows.Forms
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$dialog = New-Object System.Windows.Forms.FolderBrowserDialog
$dialog.Description = '选择异环安装根目录，或选择包含 HTGame.exe 的 Win64 文件夹'
$dialog.ShowNewFolderButton = $false
$form = New-Object System.Windows.Forms.Form
$form.TopMost = $true
$form.ShowInTaskbar = $false
$form.Width = 1
$form.Height = 1
$form.StartPosition = 'CenterScreen'
$result = $dialog.ShowDialog($form)
if ($result -eq [System.Windows.Forms.DialogResult]::OK) { Write-Output $dialog.SelectedPath }
"""
    proc = run_command(
        ["powershell", "-NoProfile", "-STA", "-ExecutionPolicy", "Bypass", "-Command", script],
        timeout=120,
    )
    if proc.returncode != 0:
        raise AppError(proc.stderr.strip() or "文件夹选择器启动失败。", 500)
    selected = proc.stdout.strip()
    return selected or None


def fetch_latest_release() -> dict:
    request = urllib.request.Request(GITHUB_RELEASE_API, headers={"User-Agent": "nte-ray-tracing-panel"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))
    assets = data.get("assets") or []
    asset = next((item for item in assets if str(item.get("name", "")).lower().endswith(".7z")), None)
    if not asset:
        raise AppError("OptiScaler 最新 Release 没有找到 .7z 资产。", 502)
    return {
        "tag": data.get("tag_name"),
        "name": data.get("name"),
        "url": data.get("html_url"),
        "published": data.get("published_at"),
        "assetName": asset.get("name"),
        "assetUrl": asset.get("browser_download_url"),
    }


def download_file(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "nte-ray-tracing-panel"})
    with urllib.request.urlopen(request, timeout=120) as response, target.open("wb") as fh:
        shutil.copyfileobj(response, fh)


def short_error(value: object, *, limit: int = 1600) -> str:
    text = str(value or "").strip()
    if not text:
        return "无详细错误。"
    if len(text) > limit:
        return text[:limit].rstrip() + "..."
    return text


def reset_extract_dir(extract_dir: Path) -> Path:
    target = ensure_under(extract_dir, TOOLS_DIR)
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=True)
    return target


def optiscaler_extract_error(archive: Path, extract_dir: Path, attempts: list[dict]) -> AppError:
    details = "\n".join(f"- {item['method']}: {item['error']}" for item in attempts)
    message = (
        "OptiScaler 已下载，但自动解压失败。\n\n"
        "原因：自动解压链路没有成功。常见情况是当前 Windows tar.exe 不支持 "
        "OptiScaler .7z 使用的 LZMA/LZMA2/BCJ2 压缩格式。\n\n"
        "你可以：\n"
        "1. 点击“重新下载/准备 OptiScaler”重试。\n"
        f"2. 或手动解压下载到的 .7z：{archive}\n"
        f"   把包含 OptiScaler.dll 和 OptiScaler.ini 的文件放到 {extract_dir} 目录。\n\n"
        f"解压尝试：\n{details}"
    )
    return AppError(message, 500)


def seven_zip_executable_candidates() -> list[str]:
    names = ("7zz.exe", "7z.exe", "7za.exe") if os.name == "nt" else ("7zz", "7z", "7za")
    candidates: list[Path] = []
    for root in (RUN_DIR, RESOURCE_DIR):
        for name in names:
            candidates.append(root / "tools" / "7zip" / name)
            candidates.append(root / name)
    for env_name in ("ProgramFiles", "ProgramFiles(x86)"):
        program_root = os.environ.get(env_name)
        if program_root:
            for name in names:
                candidates.append(Path(program_root) / "7-Zip" / name)

    resolved: list[str] = []
    seen = set()
    for candidate in candidates:
        if candidate.is_file():
            text = str(candidate)
            key = text.lower()
            if key not in seen:
                seen.add(key)
                resolved.append(text)
    for name in names:
        found = shutil.which(name)
        if found:
            key = found.lower()
            if key not in seen:
                seen.add(key)
                resolved.append(found)
    return resolved


def extract_with_py7zz(archive: Path, extract_dir: Path) -> None:
    import logging
    import py7zz

    logging.getLogger("py7zz").setLevel(logging.WARNING)
    with py7zz.SevenZipFile(archive, mode="r") as seven_zip:
        seven_zip.extractall(path=str(extract_dir))


def extract_with_py7zr(archive: Path, extract_dir: Path) -> None:
    import py7zr

    with py7zr.SevenZipFile(archive, mode="r") as seven_zip:
        seven_zip.extractall(path=str(extract_dir))


def extract_with_7zip_command(executable: str, archive: Path, extract_dir: Path) -> None:
    proc = run_command([executable, "x", "-y", f"-o{extract_dir}", str(archive)], timeout=180)
    if proc.returncode != 0:
        raise RuntimeError(short_error(proc.stderr or proc.stdout or "7-Zip 解压失败。"))


def extract_archive(archive: Path, extract_dir: Path) -> dict:
    attempts: list[dict] = []

    if archive.name.lower().endswith(".7z"):
        try:
            reset_extract_dir(extract_dir)
            extract_with_py7zz(archive, extract_dir)
            return {"method": "py7zz", "fallbacks": attempts}
        except Exception as exc:
            attempts.append({"method": "py7zz", "error": short_error(exc)})
        try:
            reset_extract_dir(extract_dir)
            extract_with_py7zr(archive, extract_dir)
            return {"method": "py7zr", "fallbacks": attempts}
        except Exception as exc:
            attempts.append({"method": "py7zr", "error": short_error(exc)})

        seven_zip_candidates = seven_zip_executable_candidates()
        for executable in seven_zip_candidates:
            try:
                reset_extract_dir(extract_dir)
                extract_with_7zip_command(executable, archive, extract_dir)
                return {"method": f"7-Zip ({Path(executable).name})", "fallbacks": attempts}
            except Exception as exc:
                attempts.append({"method": f"7-Zip ({executable})", "error": short_error(exc)})
        if not seven_zip_candidates:
            attempts.append({"method": "7-Zip executable", "error": "未找到 bundled 或已安装的 7z.exe / 7zz.exe。"})

    tar = shutil.which("tar")
    if tar:
        try:
            reset_extract_dir(extract_dir)
            proc = run_command([tar, "-xf", str(archive), "-C", str(extract_dir)], timeout=180)
            if proc.returncode != 0:
                raise RuntimeError(short_error(proc.stderr or proc.stdout or "tar.exe 解压失败。"))
            return {"method": "tar.exe", "fallbacks": attempts}
        except Exception as exc:
            attempts.append({"method": "tar.exe", "error": short_error(exc)})
    else:
        attempts.append({"method": "tar.exe", "error": "未找到 Windows tar.exe。"})

    reset_extract_dir(extract_dir)
    raise optiscaler_extract_error(archive, extract_dir, attempts)


def find_optiscaler_stage() -> dict | None:
    if not TOOLS_DIR.is_dir():
        return None
    candidates = []
    for folder in TOOLS_DIR.iterdir():
        if not folder.is_dir():
            continue
        dll = next(folder.rglob("OptiScaler.dll"), None)
        ini = next(folder.rglob("OptiScaler.ini"), None)
        if dll and ini:
            candidates.append((folder.stat().st_mtime, folder, dll, ini))
    if not candidates:
        return None
    _, folder, dll, ini = sorted(candidates, reverse=True)[0]
    return {"dir": str(folder), "dll": str(dll), "ini": str(ini), "tag": folder.name}


def ensure_optiscaler(force: bool = False) -> dict:
    existing = find_optiscaler_stage()
    if existing and not force:
        existing["downloaded"] = False
        return existing
    release = fetch_latest_release()
    archive = TOOLS_DIR / str(release["assetName"])
    extract_dir = TOOLS_DIR / str(release["tag"])
    if force and extract_dir.exists():
        ensure_under(extract_dir, TOOLS_DIR)
        shutil.rmtree(extract_dir)
    if force or not archive.is_file():
        download_file(str(release["assetUrl"]), archive)
    extraction = extract_archive(archive, extract_dir)
    stage = find_optiscaler_stage()
    if not stage:
        raise AppError("OptiScaler 已下载但未找到 OptiScaler.dll。", 500)
    stage.update({"downloaded": True, "release": release, "archive": str(archive), "extractor": extraction["method"]})
    return stage


def list_backups(win64: Path) -> list[dict]:
    root = win64 / BACKUP_DIR_NAME
    if not root.is_dir():
        return []
    rows = []
    for folder in sorted(root.iterdir(), reverse=True):
        manifest = folder / "manifest.json"
        if not manifest.is_file():
            continue
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        rows.append({
            "id": folder.name,
            "path": str(folder),
            "created": data.get("created"),
            "owner": data.get("owner") or data.get("tool"),
            "runtimeLayout": data.get("runtimeLayout"),
            "mode": data.get("mode"),
            "profile": data.get("profile", {}).get("label") or data.get("profile", {}).get("gpuName"),
            "operations": data.get("operations", []),
        })
    return rows


def read_ini_values(path: Path) -> dict:
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    wanted = {
        "SpoofedGPUName",
        "SpoofedVendorId",
        "SpoofedDeviceId",
        "TargetVendorId",
        "TargetDeviceId",
        "StreamlineSpoofing",
        "Dxgi",
        "DxgiVRAM",
        "Registry",
        "User32",
        "UseFakenvapi",
        "TargetProcessName",
        "OptiDllPath",
        "HookOriginalNvngxOnly",
    }
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r"\s*([A-Za-z0-9_]+)\s*=\s*(.*)\s*$", line)
        if match and match.group(1) in wanted:
            values[match.group(1)] = match.group(2)
    return values


def read_log_summary(path: Path) -> dict:
    if not path.is_file():
        return {"exists": False, "loaded": False, "spoofMentioned": False, "tail": ""}
    text = path.read_text(encoding="utf-8", errors="replace")
    tail = "\n".join(text.splitlines()[-120:])
    return {
        "exists": True,
        "size": path.stat().st_size,
        "modified": path.stat().st_mtime,
        "loaded": "OptiScaler" in text,
        "spoofMentioned": "Spoof" in text or "spoof" in text,
        "tail": tail,
    }


def file_summary(path: Path) -> dict:
    if not path.is_file():
        return {"exists": False}
    return {
        "exists": True,
        "size": path.stat().st_size,
        "modified": path.stat().st_mtime,
        "sha256": sha256(path),
    }


def inspect_install(win64: Path) -> dict:
    winmm = win64 / "winmm.dll"
    opt_ini = win64 / "OptiScaler.ini"
    opt_dir = win64 / "OptiScaler"
    nvngx = win64 / "nvngx.dll"
    dlsstweaks_ini = win64 / "dlsstweaks.ini"
    winmm_info = None
    if winmm.is_file():
        winmm_info = {
            "size": winmm.stat().st_size,
            "modified": winmm.stat().st_mtime,
            "sha256": sha256(winmm),
            "looksLikeOptiScaler": looks_like_optiscaler_proxy(winmm),
        }
    dlss_panel_installed = nvngx.is_file() and dlsstweaks_ini.is_file()
    info = {
        "win64": str(win64),
        "installed": bool(winmm_info and winmm_info["looksLikeOptiScaler"] and opt_ini.is_file()),
        "runtimeLayout": RUNTIME_LAYOUT,
        "managedBy": MANIFEST_OWNER,
        "winmm": winmm_info,
        "optScalerIni": read_ini_values(opt_ini),
        "optScalerDirExists": opt_dir.is_dir(),
        "log": read_log_summary(win64 / "OptiScaler.log"),
        "dlssPanel": {
            "installed": dlss_panel_installed,
            "status": (
                "检测到 nvngx.dll + dlsstweaks.ini；DLSS Panel 已安装，RT Panel 只显示兼容状态，不接管这些文件。"
                if dlss_panel_installed
                else "未检测到 nvngx.dll + dlsstweaks.ini 的 DLSS Panel 布局。"
            ),
            "nvngx": file_summary(nvngx),
            "dlsstweaksIni": file_summary(dlsstweaks_ini),
        },
    }
    return info


def backup_path_for(rel: str, backup_dir: Path) -> Path:
    return backup_dir / "files" / rel


def backup_item(game_dir: Path, rel: str, backup_dir: Path, *, kind: str) -> dict:
    source = ensure_under(game_dir / rel, game_dir)
    record = {
        "rel": rel,
        "kind": kind,
        "owner": MANIFEST_OWNER,
        "runtimeLayout": RUNTIME_LAYOUT,
        "existed": source.exists(),
    }
    if not source.exists():
        return record
    destination = backup_path_for(rel, backup_dir)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        shutil.copytree(source, destination)
        record["backupRel"] = str(Path("files") / rel)
    else:
        shutil.copy2(source, destination)
        record.update({
            "backupRel": str(Path("files") / rel),
            "size": source.stat().st_size,
            "sha256": sha256(source),
        })
    return record


def current_target_looks_rt_owned(target: Path, rel: str) -> bool:
    rel = normalize_rel(rel)
    if not target.exists():
        return True
    if rel == "winmm.dll":
        return looks_like_optiscaler_proxy(target)
    if rel == "optiscaler.ini":
        return looks_like_rt_optiscaler_ini(target)
    if rel == "optiscaler.log":
        return looks_like_optiscaler_log(target)
    if rel == "optiscaler":
        return looks_like_optiscaler_dir(target)
    return False


def restore_record_allowed(record: dict) -> tuple[bool, str | None]:
    rel = str(record.get("rel", ""))
    if not rel:
        return False, "跳过未知记录：缺少 rel"
    if is_dlss_panel_rel(rel):
        return False, f"跳过 {rel}：DLSS Panel 文件不由 RT Panel 恢复"
    if not is_canonical_managed_rel(rel):
        return False, f"跳过 {rel}：不属于当前 RT Panel runtime layout"
    owner = record.get("owner")
    if owner and owner != MANIFEST_OWNER:
        return False, f"跳过 {rel}：manifest owner={owner}"
    return True, None


def restore_item(game_dir: Path, backup_dir: Path, record: dict) -> str:
    allowed, reason = restore_record_allowed(record)
    if not allowed:
        return reason or "跳过未知记录"
    rel = record["rel"]
    target = ensure_under(game_dir / rel, game_dir)
    installed = record.get("installed")
    if target.exists():
        if installed:
            safe_to_replace = fingerprint_matches(target, installed)
            if not safe_to_replace and normalize_rel(rel) == "optiscaler.log":
                safe_to_replace = looks_like_optiscaler_log(target)
        else:
            safe_to_replace = current_target_looks_rt_owned(target, rel)
        if not safe_to_replace:
            return f"跳过 {rel}：当前目标不像本工具写入的版本，避免覆盖其他文件"
    if target.exists():
        if target.is_dir():
            shutil.rmtree(target)
        else:
            target.unlink()
    if record.get("existed") and record.get("backupRel"):
        source = ensure_under(backup_dir / record["backupRel"], backup_dir)
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        return f"恢复 {rel}"
    return f"移除 {rel}"


def set_ini_value(lines: list[str], key: str, value: str) -> list[str]:
    pattern = re.compile(r"^\s*" + re.escape(key) + r"\s*=")
    changed = False
    out = []
    for line in lines:
        if not changed and pattern.match(line):
            out.append(f"{key}={value}")
            changed = True
        else:
            out.append(line)
    if not changed:
        out.append(f"{key}={value}")
    return out


def set_ini_section_value(lines: list[str], section: str, key: str, value: str) -> list[str]:
    key_pattern = re.compile(r"^\s*" + re.escape(key) + r"\s*=", re.IGNORECASE)
    section_pattern = re.compile(r"^\s*\[" + re.escape(section) + r"\]\s*$", re.IGNORECASE)
    cleaned = [line for line in lines if not key_pattern.match(line)]
    section_index = next((index for index, line in enumerate(cleaned) if section_pattern.match(line)), None)
    if section_index is None:
        if cleaned and cleaned[-1].strip():
            cleaned.append("")
        cleaned.extend([f"[{section}]", f"{key}={value}"])
        return cleaned
    cleaned.insert(section_index + 1, f"{key}={value}")
    return cleaned


def build_optiscaler_config(template: Path, *, mode: str, target_device_id: str | None, profile: dict) -> str:
    lines = template.read_text(encoding="utf-8", errors="replace").splitlines()
    values = {
        "SpoofedVendorId": profile["vendorId"],
        "SpoofedDeviceId": profile["deviceId"],
        "TargetVendorId": "0x10de",
        "TargetDeviceId": target_device_id or "auto",
        "SpoofedGPUName": profile["gpuName"],
        "OptiDllPath": r".\OptiScaler",
        "StreamlineSpoofing": "true",
        "Dxgi": "true",
        "DxgiFactoryWrapping": "false",
        "DxgiVRAM": profile["vramGb"],
        "Registry": "true" if mode == "full" else "false",
        "User32": "true" if mode == "full" else "false",
        "UseFakenvapi": "true" if mode == "full" else "false",
        "TargetProcessName": GAME_EXE,
        "LogToFile": "true",
        "LogLevel": "0",
        "SingleFile": "true",
        "CheckForUpdate": "false",
    }
    if mode == "full":
        values["NvapiPath"] = r".\OptiScaler\fakenvapi.dll"
    for key, value in values.items():
        lines = set_ini_value(lines, key, value)
    lines = set_ini_section_value(lines, "Hooks", "HookOriginalNvngxOnly", "true")
    return "\n".join(lines).rstrip() + "\n"


def copy_optiscaler_payload(stage: dict, game_dir: Path) -> None:
    dll = Path(stage["dll"])
    ini = Path(stage["ini"])
    release_root = dll.parent
    winmm = game_dir / "winmm.dll"
    shutil.copy2(dll, winmm)
    if sha256(dll) != sha256(winmm) or not looks_like_optiscaler_proxy(winmm):
        raise AppError("winmm.dll 写入后校验失败：目标不是 OptiScaler 代理。", 500)
    opt_dir = game_dir / "OptiScaler"
    if opt_dir.exists():
        shutil.rmtree(opt_dir)
    opt_dir.mkdir(parents=True, exist_ok=True)
    for item in release_root.iterdir():
        if item.name in {"OptiScaler.dll", "OptiScaler.ini", "Licenses"}:
            continue
        if item.is_file() and item.suffix.lower() in {".dll", ".ini"}:
            shutil.copy2(item, opt_dir / item.name)
        elif item.is_dir() and item.name == "D3D12_Optiscaler":
            shutil.copytree(item, opt_dir / item.name)
    shutil.copy2(ini, opt_dir / "_source_OptiScaler.ini")


def install_spoof(
    path_value: str,
    *,
    mode: str = "dxgi",
    profile_id: str | None = None,
    close_game: bool = False,
    force_download: bool = False,
) -> dict:
    mode = mode.lower()
    if mode not in {"dxgi", "full"}:
        raise AppError("模式无效。")
    running = running_processes()
    if running:
        if not close_game:
            raise AppError("检测到异环或启动器正在运行。请先关闭，或勾选自动关闭后再安装。")
        close_game_processes()
    detected = detect_game(path_value)
    win64 = Path(detected["win64"])
    stage = ensure_optiscaler(force_download)
    adapters = get_nvidia_adapters()
    target_device_id = adapters[0].get("DeviceIdHex") if adapters else None
    profile = resolve_profile(profile_id, adapters)

    backup_dir = win64 / BACKUP_DIR_NAME / now_id()
    backup_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "created": datetime.now().isoformat(timespec="seconds"),
        "tool": MANIFEST_OWNER,
        "owner": MANIFEST_OWNER,
        "version": APP_VERSION,
        "runtimeLayout": RUNTIME_LAYOUT,
        "managedFiles": list(MANAGED_FILES),
        "managedDirs": list(MANAGED_DIRS),
        "dlssPanelDetected": (win64 / "nvngx.dll").is_file() and (win64 / "dlsstweaks.ini").is_file(),
        "mode": mode,
        "profile": profile,
        "win64": str(win64),
        "stage": stage,
        "targetDeviceId": target_device_id,
        "items": [],
        "operations": [],
    }
    for rel in MANAGED_FILES:
        manifest["items"].append(backup_item(win64, rel, backup_dir, kind="file"))
    for rel in MANAGED_DIRS:
        manifest["items"].append(backup_item(win64, rel, backup_dir, kind="dir"))
    manifest["operations"].append("创建安装前备份")

    copy_optiscaler_payload(stage, win64)
    manifest["operations"].append("写入 winmm.dll OptiScaler 代理")
    manifest["operations"].append("写入 OptiScaler 依赖目录")
    config = build_optiscaler_config(Path(stage["ini"]), mode=mode, target_device_id=target_device_id, profile=profile)
    (win64 / "OptiScaler.ini").write_text(config, encoding="ascii", errors="ignore")
    manifest["operations"].append(f"写入 OptiScaler.ini GPU spoof 配置: {profile['label']}")
    manifest["operations"].append("强制 [Hooks] HookOriginalNvngxOnly=true")
    (win64 / "OptiScaler.log").write_text("", encoding="utf-8")
    manifest["operations"].append("初始化 OptiScaler.log")
    for record in manifest["items"]:
        record["installed"] = item_fingerprint(win64 / record["rel"])

    (backup_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "ok": True,
        "message": "已备份并安装光追解锁配置。",
        "backup": str(backup_dir),
        "mode": mode,
        "profile": profile,
        "targetDeviceId": target_device_id,
        "detected": detect_game(path_value),
    }


def restore_backup(path_value: str, backup_id: str | None, *, close_game: bool = False) -> dict:
    running = running_processes()
    if running:
        if not close_game:
            raise AppError("检测到异环或启动器正在运行。请先关闭，或勾选自动关闭后再恢复。")
        close_game_processes()
    detected = detect_game(path_value)
    win64 = Path(detected["win64"])
    backups = list_backups(win64)
    if not backups:
        raise AppError("没有找到可恢复备份。")
    selected_id = backup_id or backups[0]["id"]
    backup_dir = ensure_under(win64 / BACKUP_DIR_NAME / selected_id, win64 / BACKUP_DIR_NAME)
    manifest_path = backup_dir / "manifest.json"
    if not manifest_path.is_file():
        raise AppError("备份 manifest.json 不存在。")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    operations = []
    for record in manifest.get("items", []):
        operations.append(restore_item(win64, backup_dir, record))
    return {
        "ok": True,
        "message": f"已恢复备份 {selected_id}。",
        "operations": operations,
        "detected": detect_game(path_value),
    }


def api_state(path_value: str | None = None) -> dict:
    common = None
    selected = None
    adapters = get_nvidia_adapters()
    if path_value:
        try:
            selected = detect_game(path_value)
        except AppError as exc:
            selected = {"error": str(exc)}
    if not selected:
        common = detect_common_game()
    return {
        "version": APP_VERSION,
        "name": APP_CN_NAME,
        "fullName": APP_FULL_CN_NAME,
        "englishName": APP_EN_NAME,
        "keywords": APP_SEARCH_KEYWORDS,
        "runDir": str(RUN_DIR),
        "toolsDir": str(TOOLS_DIR),
        "processes": running_processes(),
        "procmon": procmon_filter_state(),
        "nvidia": adapters,
        "profiles": spoof_profiles(adapters),
        "defaultProfile": DEFAULT_PROFILE_ID,
        "optiscaler": find_optiscaler_stage(),
        "commonDetected": common,
        "selectedDetected": selected,
    }


def schedule_shutdown(server: ThreadingHTTPServer) -> None:
    def worker() -> None:
        time.sleep(0.35)
        server.shutdown()

    threading.Thread(target=worker, daemon=True).start()


class Handler(BaseHTTPRequestHandler):
    server_version = f"NTERayTracingPanel/{APP_VERSION}"

    def log_message(self, fmt: str, *args: object) -> None:
        safe_log("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def send_json(self, data: object, status: int = 200) -> None:
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        try:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise AppError("请求 JSON 无效。") from exc

    def handle_error(self, exc: Exception) -> None:
        if isinstance(exc, AppError):
            self.send_json({"ok": False, "error": str(exc)}, exc.status)
        else:
            self.send_json({"ok": False, "error": f"内部错误: {exc}"}, 500)

    def do_GET(self) -> None:
        try:
            parsed = urlparse(self.path)
            if parsed.path == "/api/state":
                query = parse_qs(parsed.query)
                self.send_json({"ok": True, **api_state(query.get("path", [None])[0])})
                return
            if parsed.path == "/api/log":
                query = parse_qs(parsed.query)
                detected = detect_game(query.get("path", [None])[0])
                log = read_log_summary(Path(detected["win64"]) / "OptiScaler.log")
                self.send_json({"ok": True, "log": log})
                return
            rel = unquote(parsed.path.lstrip("/")) or "index.html"
            target = (WEB_DIR / rel).resolve()
            if not str(target).startswith(str(WEB_DIR.resolve())) or not target.is_file():
                target = WEB_DIR / "index.html"
            content = target.read_bytes()
            mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except Exception as exc:
            self.handle_error(exc)

    def do_POST(self) -> None:
        try:
            parsed = urlparse(self.path)
            data = self.read_json()
            if parsed.path == "/api/browse":
                selected = run_folder_dialog()
                self.send_json({"ok": True, "path": selected, "cancelled": selected is None})
                return
            if parsed.path == "/api/detect":
                self.send_json({"ok": True, "detected": detect_game(data.get("path"))})
                return
            if parsed.path == "/api/download":
                self.send_json({"ok": True, "optiscaler": ensure_optiscaler(bool(data.get("force")))})
                return
            if parsed.path == "/api/install":
                self.send_json(install_spoof(
                    data.get("path"),
                    mode=data.get("mode") or "dxgi",
                    profile_id=data.get("profile") or data.get("profileId"),
                    close_game=bool(data.get("closeGame")),
                    force_download=bool(data.get("forceDownload")),
                ))
                return
            if parsed.path == "/api/restore":
                self.send_json(restore_backup(
                    data.get("path"),
                    data.get("backup"),
                    close_game=bool(data.get("closeGame")),
                ))
                return
            if parsed.path == "/api/shutdown":
                self.send_json({"ok": True, "message": "后端服务正在退出。"})
                schedule_shutdown(self.server)
                return
            raise AppError("未知 API。", 404)
        except Exception as exc:
            self.handle_error(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description="NTE Ray Tracing Panel")
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if not WEB_DIR.is_dir():
        safe_log("web directory missing", error=True)
        return 1
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    url = f"http://{args.host}:{args.port}/"
    safe_log(f"NTE Ray Tracing Panel {APP_VERSION} running at {url}")
    if not args.no_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        safe_log("Stopping...")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
