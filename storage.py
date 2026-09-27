# -*- coding: utf-8 -*-
"""
storage.py
Small JSON-backed persistence layer for user settings and transcription
history. Everything lives under ~/.voice_to_text_cli/ so the tool works
the same regardless of where it's launched from.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

APP_DIR = Path.home() / ".voice_to_text_cli"
CONFIG_PATH = APP_DIR / "config.json"
HISTORY_PATH = APP_DIR / "history.json"

DEFAULT_CONFIG: Dict[str, Any] = {
    "ui_language": None,          # "en" or "fa" — None means "ask every time"
    "default_model": "small",
    "default_source_lang": "auto",
    "default_output_dir": str(Path.home() / "Transcripts"),
}


def _ensure_app_dir() -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict[str, Any]:
    _ensure_app_dir()
    if not CONFIG_PATH.exists():
        return dict(DEFAULT_CONFIG)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = dict(DEFAULT_CONFIG)
        merged.update(data or {})
        return merged
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_CONFIG)


def save_config(config: Dict[str, Any]) -> None:
    _ensure_app_dir()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_history() -> List[Dict[str, Any]]:
    _ensure_app_dir()
    if not HISTORY_PATH.exists():
        return []
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f) or []
    except (json.JSONDecodeError, OSError):
        return []


def save_history(entries: List[Dict[str, Any]]) -> None:
    _ensure_app_dir()
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


def add_history_entry(entry: Dict[str, Any]) -> None:
    entries = load_history()
    entry.setdefault("timestamp", datetime.now().isoformat(timespec="seconds"))
    entries.append(entry)
    save_history(entries)


def clear_history() -> None:
    save_history([])
