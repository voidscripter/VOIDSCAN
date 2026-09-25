"""Operating system and host details."""

from __future__ import annotations

import platform
import socket
from pathlib import Path


def _os_release() -> dict[str, str]:
    values: dict[str, str] = {}
    try:
        for line in Path("/etc/os-release").read_text(encoding="utf-8").splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                values[key] = value.strip().strip('"')
    except OSError:
        pass
    return values


def collect_system() -> dict[str, str]:
    release = _os_release()
    uptime = "N/A"
    try:
        seconds = float(Path("/proc/uptime").read_text().split()[0])
        days, rem = divmod(int(seconds), 86400)
        hours, rem = divmod(rem, 3600)
        minutes = rem // 60
        uptime = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"
    except (OSError, ValueError, IndexError):
        pass
    return {
        "operating_system": platform.system() or "N/A",
        "distribution": release.get("PRETTY_NAME", release.get("NAME", "N/A")),
        "kernel": platform.release() or "N/A",
        "hostname": socket.gethostname() or "N/A",
        "architecture": platform.machine() or "N/A",
        "uptime": uptime,
    }
