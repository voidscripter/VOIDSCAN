"""Command line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from rich.console import Console

from voidscan import __version__
from voidscan.display import render, render_subset
from voidscan.hardware import collect_hardware
from voidscan.network import collect_network
from voidscan.performance import collect_performance
from voidscan.report import write_report
from voidscan.system import collect_system


def collect_all() -> dict[str, object]:
    return {
        "system": collect_system(),
        "hardware": collect_hardware(),
        "performance": collect_performance(),
        "network": collect_network(),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="voidscan", description="A read-only Linux system analyzer.")
    parser.add_argument("--version", action="version", version=f"voidscan {__version__}")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--hardware", action="store_true", help="Show hardware information")
    group.add_argument("--performance", action="store_true", help="Show current performance information")
    group.add_argument("--network", action="store_true", help="Show network information")
    group.add_argument("--report", action="store_true", help="Write a JSON report to voidscan-report.json")
    args = parser.parse_args(argv)
    console = Console()
    try:
        data = collect_all()
        if args.report:
            path = write_report(data)
            console.print(f"[green]Report written:[/] {path.resolve()}")
        elif args.hardware:
            render_subset("HARDWARE", data, console)
        elif args.performance:
            render_subset("PERFORMANCE", data, console)
        elif args.network:
            render_subset("NETWORK", data, console)
        else:
            render(data, console)
        return 0
    except (OSError, PermissionError) as error:
        Console(file=sys.stderr).print(f"[red]Unable to complete scan:[/] {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
