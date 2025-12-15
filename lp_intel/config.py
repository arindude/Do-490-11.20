from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Iterable, Sequence

from .models import Source, ensure_iterable

try:
    import yaml
except Exception:  # pragma: no cover - dependency hint only
    yaml = None


DATA_DIR = Path(__file__).resolve().parent / "data"
RAW_DIR = DATA_DIR / "raw"
TEXT_DIR = DATA_DIR / "text"
DEFAULT_DB = DATA_DIR / "insights.db"
DEFAULT_SOURCES = Path(__file__).resolve().parent / "config" / "sources.yml"

# Simple keyword lists used by the classifier. Adjust per institution or strategy.
KEYWORDS = {
    "rfp": ("request for proposal", "rfp", "solicitation", "manager search"),
    "allocation": ("allocation", "commitment", "commitments", "pacing", "plan"),
    "strategy": ("strategy", "focus", "priority", "emerging markets", "core", "value-add", "opportunistic"),
    "performance": ("performance", "benchmark", "returns", "irr", "distribution", "valuation"),
}


def _load_yaml(path: Path):
    if yaml is None:
        raise RuntimeError("PyYAML is required to load YAML source files. Install with `pip install pyyaml`.")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or []


def load_sources(path: Path | None = None) -> Sequence[Source]:
    path = path or DEFAULT_SOURCES
    if not path.exists():
        raise FileNotFoundError(f"Source file not found at {path}")
    data = _load_yaml(path) if path.suffix in {".yml", ".yaml"} else json.loads(path.read_text())
    sources: list[Source] = []
    for item in data:
        source = Source(
            name=item["name"],
            url=item["url"],
            doc_type=item.get("doc_type", "auto"),
            enabled=bool(item.get("enabled", True)),
            notes=item.get("notes"),
            tags=ensure_iterable(item.get("tags")),
        )
        if source.enabled:
            sources.append(source)
    return sources


def timestamp_now() -> dt.datetime:
    return dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)

