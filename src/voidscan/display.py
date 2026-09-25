"""Rich terminal presentation."""

from __future__ import annotations

from typing import Any

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def _bytes(value: int | float) -> str:
    size = float(value)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def _rate(value: float) -> str:
    return f"{_bytes(value)}/s"


def _meter(percent: float) -> str:
    filled = max(0, min(10, round(percent / 10)))
    return f"[cyan]{'█' * filled}{'░' * (10 - filled)}[/]  {percent:.0f}%"


def _section(title: str, entries: list[tuple[str, str]]) -> Panel:
    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold cyan", width=16)
    table.add_column()
    for key, value in entries:
        table.add_row(key, value)
    return Panel(table, title=f"[bold white]{title}[/]", border_style="bright_blue", box=box.ROUNDED, padding=(0, 1))


def render(data: dict[str, Any], console: Console | None = None) -> None:
    console = console or Console()
    console.print(Panel(Text("VOIDSCAN\nSystem Analyzer", justify="center", style="bold bright_cyan"), box=box.DOUBLE, border_style="bright_blue", padding=(1, 4)))
    s, h, p, n = data["system"], data["hardware"], data["performance"], data["network"]
    console.print(_section("SYSTEM", [("OS", str(s["distribution"])), ("Kernel", str(s["kernel"])), ("Hostname", str(s["hostname"])), ("Architecture", str(s["architecture"])), ("Uptime", str(s["uptime"]))]))
    console.print(_section("HARDWARE", [("CPU", str(h["cpu_model"])), ("Cores / threads", f"{h['cpu_cores']} / {h['cpu_threads']}"), ("GPU", str(h["gpu"])), ("RAM", _bytes(h["ram_total_bytes"])), ("Root disk", f"{_bytes(h['disk_used_bytes'])} / {_bytes(h['disk_total_bytes'])}")]))
    freq = p["cpu_frequency_mhz"]
    temps = p["temperatures_celsius"]
    temp = ", ".join(f"{name}: {value:.1f}°C" for name, value in list(temps.items())[:3]) if isinstance(temps, dict) else "N/A"
    if isinstance(temps, dict) and len(temps) > 3:
        temp += f" (+{len(temps) - 3} sensors)"
    console.print(_section("PERFORMANCE", [("CPU", _meter(p["cpu_percent"])), ("RAM", f"{_meter(p['ram_percent'])}  {_bytes(p['ram_used_bytes'])} / {_bytes(p['ram_total_bytes'])}"), ("Disk", _meter(p["disk_percent"])), ("CPU frequency", f"{freq:.0f} MHz" if freq else "N/A"), ("Temperatures", temp)]))
    status = "N/A" if n["connected"] is None else "Connected" if n["connected"] else "Disconnected"
    console.print(_section("NETWORK", [("Status", status), ("Interface", str(n["interface"])), ("Local IP", str(n["local_ip"])), ("Download", _rate(n["download_bytes_per_second"])), ("Upload", _rate(n["upload_bytes_per_second"]))]))
    console.print("\n[bold green]✓[/] System scan completed")


def render_subset(title: str, data: dict[str, Any], console: Console | None = None) -> None:
    console = console or Console()
    if title == "HARDWARE":
        h = data["hardware"]
        entries = [("CPU", str(h["cpu_model"])), ("Cores / threads", f"{h['cpu_cores']} / {h['cpu_threads']}"), ("GPU", str(h["gpu"])), ("RAM", _bytes(h["ram_total_bytes"])), ("Root disk", f"{_bytes(h['disk_used_bytes'])} / {_bytes(h['disk_total_bytes'])}")]
    elif title == "PERFORMANCE":
        p = data["performance"]
        entries = [("CPU", _meter(p["cpu_percent"])), ("RAM", _meter(p["ram_percent"])), ("Disk", _meter(p["disk_percent"])), ("CPU frequency", f"{p['cpu_frequency_mhz']:.0f} MHz" if p["cpu_frequency_mhz"] else "N/A"), ("Temperatures", str(p["temperatures_celsius"]))]
    else:
        n = data["network"]
        status = "N/A" if n["connected"] is None else "Connected" if n["connected"] else "Disconnected"
        entries = [("Status", status), ("Interface", str(n["interface"])), ("Local IP", str(n["local_ip"])), ("Download", _rate(n["download_bytes_per_second"])), ("Upload", _rate(n["upload_bytes_per_second"]))]
    console.print(_section(title, entries))
