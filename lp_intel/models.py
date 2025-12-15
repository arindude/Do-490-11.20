from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class Source:
    name: str
    url: str
    doc_type: str  # pdf, html, auto
    enabled: bool = True
    notes: str | None = None
    tags: tuple[str, ...] = ()


@dataclass
class Document:
    source: Source
    fetched_at: dt.datetime
    path: Path
    content_type: str


@dataclass
class Insight:
    doc: Document
    category: str
    excerpt: str
    context: str
    detected_at: dt.datetime
    terms: tuple[str, ...] = ()


def ensure_iterable(value: Optional[str | Iterable[str]]) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(value)

