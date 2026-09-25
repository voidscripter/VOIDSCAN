"""JSON report writing."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_report(data: dict[str, Any], destination: Path = Path("voidscan-report.json")) -> Path:
    destination.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return destination
