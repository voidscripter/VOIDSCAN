"""Read-only network interface and throughput sampling."""

from __future__ import annotations

import ipaddress
import time
from typing import Any

import psutil


def collect_network(sample_seconds: float = 0.35) -> dict[str, Any]:
    try:
        stats = psutil.net_if_stats()
        addresses = psutil.net_if_addrs()
    except (OSError, psutil.Error):
        return {"connected": None, "interface": "N/A", "local_ip": "N/A", "download_bytes_per_second": 0.0, "upload_bytes_per_second": 0.0}
    candidates: list[tuple[str, str]] = []
    for interface, info in stats.items():
        if interface == "lo" or not info.isup:
            continue
        for address in addresses.get(interface, []):
            if address.family == psutil.AF_LINK or ":" in address.address and "%" in address.address:
                continue
            try:
                ip = ipaddress.ip_address(address.address.split("%", 1)[0])
                if not ip.is_loopback and not ip.is_link_local:
                    candidates.append((interface, str(ip)))
            except ValueError:
                continue
    interface, local_ip = candidates[0] if candidates else ("N/A", "N/A")
    try:
        before = psutil.net_io_counters(pernic=True) or {}
        time.sleep(max(0.0, sample_seconds))
        after = psutil.net_io_counters(pernic=True) or {}
    except (OSError, psutil.Error):
        return {"connected": bool(candidates), "interface": interface, "local_ip": local_ip, "download_bytes_per_second": 0.0, "upload_bytes_per_second": 0.0}
    rx = tx = 0
    selected = interface if interface in before and interface in after else None
    names = [selected] if selected else [name for name in before if name in after and name != "lo"]
    for name in names:
        rx += max(0, after[name].bytes_recv - before[name].bytes_recv)
        tx += max(0, after[name].bytes_sent - before[name].bytes_sent)
    duration = max(sample_seconds, 0.001)
    return {
        "connected": bool(candidates),
        "interface": interface,
        "local_ip": local_ip,
        "download_bytes_per_second": rx / duration,
        "upload_bytes_per_second": tx / duration,
    }
