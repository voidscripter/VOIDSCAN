"""Hardware inventory helpers."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import psutil


def _cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace").splitlines():
            if line.lower().startswith(("model name", "hardware")) and ":" in line:
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return "N/A"


def _gpu() -> str:
    if shutil.which("nvidia-smi"):
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
                capture_output=True, text=True, timeout=2, check=False,
            )
            names = [line.strip() for line in result.stdout.splitlines() if line.strip()]
            if result.returncode == 0 and names:
                return ", ".join(names)
        except (OSError, subprocess.TimeoutExpired):
            pass
    # PCI display controller names are exposed by sysfs without invoking a shell.
    try:
        names = []
        for path in Path("/sys/bus/pci/devices").glob("*/class"):
            try:
                if path.read_text().strip().startswith("0x03"):
                    name = path.parent / "product_name"
                    if name.exists():
                        names.append(name.read_text().strip())
                    else:
                        vendor = (path.parent / "vendor").read_text().strip()
                        names.append({"0x10de": "NVIDIA GPU", "0x1002": "AMD GPU", "0x8086": "Intel GPU"}.get(vendor, "GPU"))
            except OSError:
                continue
        if names:
            return ", ".join(dict.fromkeys(names))
    except OSError:
        pass
    return "Not detected"


def collect_hardware() -> dict[str, object]:
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    return {
        "cpu_model": _cpu_model(),
        "cpu_cores": psutil.cpu_count(logical=False) or "N/A",
        "cpu_threads": psutil.cpu_count(logical=True) or "N/A",
        "gpu": _gpu(),
        "ram_total_bytes": vm.total,
        "disk_total_bytes": disk.total,
        "disk_used_bytes": disk.used,
        "root_filesystem": {"total_bytes": disk.total, "used_bytes": disk.used, "free_bytes": disk.free, "percent": disk.percent},
    }
