# -*- coding: utf-8 -*-
"""
exporters.py
Turn a list of transcript segments into various on-disk formats.

Each segment is expected to be a dict with keys: "start", "end", "text"
(seconds as floats, text as str) — see transcriber.Segment.
"""
import json
from pathlib import Path
from typing import Any, Dict, List


def _format_timestamp(seconds: float, comma: bool) -> str:
    if seconds < 0:
        seconds = 0
    ms_total = round(seconds * 1000)
    hours, rem = divmod(ms_total, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, ms = divmod(rem, 1000)
    sep = "," if comma else "."
    return f"{hours:02d}:{minutes:02d}:{secs:02d}{sep}{ms:03d}"


def build_txt(segments: List[Dict[str, Any]]) -> str:
    return " ".join(seg["text"].strip() for seg in segments).strip()


def build_srt(segments: List[Dict[str, Any]]) -> str:
    lines = []
    for i, seg in enumerate(segments, start=1):
        lines.append(str(i))
        start = _format_timestamp(seg["start"], comma=True)
        end = _format_timestamp(seg["end"], comma=True)
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_vtt(segments: List[Dict[str, Any]]) -> str:
    lines = ["WEBVTT", ""]
    for seg in segments:
        start = _format_timestamp(seg["start"], comma=False)
        end = _format_timestamp(seg["end"], comma=False)
        lines.append(f"{start} --> {end}")
        lines.append(seg["text"].strip())
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def build_json(segments: List[Dict[str, Any]], meta: Dict[str, Any]) -> str:
    payload = {"metadata": meta, "segments": segments}
    return json.dumps(payload, ensure_ascii=False, indent=2)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
