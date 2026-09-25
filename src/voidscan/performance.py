"""Current resource usage and available sensor readings."""

from __future__ import annotations

from typing import Any

import psutil


def collect_performance() -> dict[str, Any]:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    frequency = psutil.cpu_freq()
    temperatures: dict[str, float] = {}
    try:
        for group, readings in (psutil.sensors_temperatures() or {}).items():
            for sensor in readings:
                if sensor.current is not None:
                    temperatures[sensor.label or group] = sensor.current
    except (AttributeError, OSError):
        pass
    return {
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "ram_percent": memory.percent,
        "ram_used_bytes": memory.used,
        "ram_total_bytes": memory.total,
        "disk_percent": disk.percent,
        "cpu_frequency_mhz": frequency.current if frequency else None,
        "temperatures_celsius": temperatures or "N/A",
    }
