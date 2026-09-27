#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice to Text — a bilingual (English/Persian) terminal transcription studio.

Interactive mode:
    python main.py

Scriptable / non-interactive mode:
    python main.py --file audio.mp3 --model small --lang en --formats txt,srt

Originally a 17-line script (github.com/amirtahanemati/voice-to-text) that
loaded Whisper and transcribed a single hardcoded file. This version wraps
that same idea in a full terminal app: language picker, arrow-key menus,
live progress + transcript preview, microphone recording, batch folders,
history, settings, and multi-format export.
"""
import argparse
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

import questionary
from questionary import Choice
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn,
    TimeElapsedColumn, TaskProgressColumn,
)
from rich.table import Table
from rich.panel import Panel

import storage
import exporters
import transcriber
from transcriber import MODEL_SIZES
from i18n import t
from ui import console, print_banner, rule, panel, success, warn, error, info, kv

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

try:
    import recorder
except Exception:
    recorder = None


QSTYLE = questionary.Style([
    ("qmark", "fg:#d787ff bold"),
    ("question", "bold"),
    ("pointer", "fg:#00d7ff bold"),
    ("highlighted", "fg:#00d7ff bold"),
    ("selected", "fg:#5fff87 bold"),
])


# --------------------------------------------------------------------------
# Language / setup
# --------------------------------------------------------------------------

def choose_ui_language(config: dict) -> str:
    if config.get("ui_language") in ("en", "fa"):
        return config["ui_language"]

    choice = questionary.select(
        "Choose your language / زبان خود را انتخاب کنید",
        choices=[
            Choice(title="English", value="en"),
            Choice(title="فارسی (Persian)", value="fa"),
        ],
        style=QSTYLE,
    ).ask()

    if choice is None:
        sys.exit(0)

    config["ui_language"] = choice
    storage.save_config(config)
    return choice


def word_count(text: str) -> int:
    return len(text.split())


def human_seconds(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:d}:{s:02d}"


# --------------------------------------------------------------------------
# Core transcription flow (shared by file / record / batch)
# --------------------------------------------------------------------------

SOURCE_LANG_MAP = {
    "auto": None,
    "en": "en",
    "fa": "fa",
}


def pick_model(lang: str, default: str) -> str:
    labels = {
        "tiny": t(lang, "model_tiny"),
        "base": t(lang, "model_base"),
        "small": t(lang, "model_small"),
        "medium": t(lang, "model_medium"),
        "large-v3": t(lang, "model_large"),
    }
    choices = [Choice(title=labels[m], value=m) for m in MODEL_SIZES]
    return questionary.select(
        t(lang, "choose_model_prompt"),
        choices=choices,
        default=next((c for c in choices if c.value == default), None),
        style=QSTYLE,
    ).ask()


def pick_source_lang(lang: str, default: str = "auto") -> str:
    choices = [
        Choice(title=t(lang, "lang_auto"), value="auto"),
        Choice(title=t(lang, "lang_english"), value="en"),
        Choice(title=t(lang, "lang_persian"), value="fa"),
        Choice(title=t(lang, "lang_other"), value="other"),
    ]
    picked = questionary.select(
        t(lang, "choose_source_lang_prompt"),
        choices=choices,
        style=QSTYLE,
    ).ask()
    if picked == "other":
        code = questionary.text(t(lang, "enter_lang_code_prompt"), style=QSTYLE).ask()
        return (code or "auto").strip().lower()
    return picked


def pick_export_formats(lang: str) -> list:
    choices = [
        Choice(title=t(lang, "format_txt"), value="txt", checked=True),
        Choice(title=t(lang, "format_srt"), value="srt"),
        Choice(title=t(lang, "format_vtt"), value="vtt"),
        Choice(title=t(lang, "format_json"), value="json"),
    ]
    result = questionary.checkbox(
        t(lang, "ask_more_formats"), choices=choices, style=QSTYLE
    ).ask()
    return result or ["txt"]


def run_transcription(lang: str, audio_path: Path, model_size: str,
                       source_lang: str, output_dir: Path, config: dict) -> bool:
    if not audio_path.exists():
        error(t(lang, "file_not_found", path=str(audio_path)))
        return False

    info(t(lang, "loading_model", model=model_size))
    try:
        model = transcriber.load_model(model_size)
    except Exception as exc:
        error(t(lang, "error_generic", error=str(exc)))
        return False
    success(t(lang, "model_ready"))

    if transcriber.gpu_available():
        info(t(lang, "gpu_found"))
    else:
        info(t(lang, "no_gpu"))

    rule(t(lang, "live_preview_title"))

    start_time = time.time()
    segments = []
    detected_info = {}

    with Progress(
        SpinnerColumn(),
        TextColumn("[accent]" + t(lang, "transcribing_label") + "[/accent]"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    ) as progress:
        task = progress.add_task("transcribe", total=100)

        def on_segment(seg, fraction):
            progress.console.print(f"[muted]{seg.text.strip()}[/muted]")
            progress.update(task, completed=fraction * 100)

        try:
            seg_objs, tinfo = transcriber.transcribe_stream(
                model, str(audio_path),
                language=SOURCE_LANG_MAP.get(source_lang, source_lang),
                on_segment=on_segment,
            )
        except Exception as exc:
            progress.stop()
            error(t(lang, "error_generic", error=str(exc)))
            return False

        progress.update(task, completed=100)

    segments = [s.as_dict() for s in seg_objs]
    elapsed = time.time() - start_time
    full_text = exporters.build_txt(segments)

    success(t(lang, "transcription_done"))
    console.print()

    # Stats panel
    rule(t(lang, "stats_title"))
    kv(t(lang, "stats_duration"), human_seconds(tinfo.duration))
    kv(t(lang, "stats_words"), str(word_count(full_text)))
    kv(t(lang, "stats_elapsed"), human_seconds(elapsed))
    if elapsed > 0:
        kv(t(lang, "stats_speed"), f"{tinfo.duration / elapsed:.1f}x realtime")
    console.print()

    # Export
    formats = pick_export_formats(lang)
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem
    saved_paths = []
    for fmt in formats:
        out_path = output_dir / f"{stem}.{fmt}"
        if fmt == "txt":
            exporters.write_file(out_path, full_text)
        elif fmt == "srt":
            exporters.write_file(out_path, exporters.build_srt(segments))
        elif fmt == "vtt":
            exporters.write_file(out_path, exporters.build_vtt(segments))
        elif fmt == "json":
            meta = {
                "source_file": str(audio_path),
                "language": tinfo.language,
                "language_probability": tinfo.language_probability,
                "duration_seconds": tinfo.duration,
                "model": model_size,
            }
            exporters.write_file(out_path, exporters.build_json(segments, meta))
        saved_paths.append(out_path)

    for p in saved_paths:
        success(f'{t(lang, "stats_output")}: {p}')

    # Clipboard
    if CLIPBOARD_AVAILABLE:
        if questionary.confirm(t(lang, "copy_clipboard_prompt"), default=False, style=QSTYLE).ask():
            pyperclip.copy(full_text)
            success(t(lang, "copied_clipboard"))
    else:
        warn(t(lang, "clipboard_unavailable"))

    # History
    storage.add_history_entry({
        "source_file": str(audio_path),
        "output_files": [str(p) for p in saved_paths],
        "model": model_size,
        "language": tinfo.language,
        "duration_seconds": tinfo.duration,
        "word_count": word_count(full_text),
        "elapsed_seconds": elapsed,
    })

    return True


# --------------------------------------------------------------------------
# Menu handlers
# --------------------------------------------------------------------------

def handle_transcribe_file(lang: str, config: dict):
    rule(t(lang, "menu_transcribe_file"))
    path_str = questionary.path(t(lang, "file_path_prompt"), style=QSTYLE).ask()
    if not path_str:
        return
    audio_path = Path(path_str).expanduser()
    if not audio_path.exists():
        error(t(lang, "file_not_found", path=path_str))
        return
    if not transcriber.is_supported_file(str(audio_path)):
        warn(t(lang, "unsupported_file", path=path_str))
        if not questionary.confirm("Continue anyway?", default=False, style=QSTYLE).ask():
            return

    model_size = pick_model(lang, config["default_model"])
    source_lang = pick_source_lang(lang, config["default_source_lang"])
    output_dir = Path(config["default_output_dir"]).expanduser()

    run_transcription(lang, audio_path, model_size, source_lang, output_dir, config)


def handle_record(lang: str, config: dict):
    rule(t(lang, "menu_record"))
    if recorder is None or not recorder.RECORDING_AVAILABLE:
        warn(t(lang, "recording_unavailable"))
        return

    info(t(lang, "record_instructions"))
    questionary.press_any_key_to_continue(t(lang, "press_enter_continue")).ask()

    rec_dir = Path(config["default_output_dir"]).expanduser() / "recordings"
    rec_path = rec_dir / f"recording_{datetime.now():%Y%m%d_%H%M%S}.wav"

    console.print(f"[warn]● {t(lang, 'recording_started')}[/warn]")
    try:
        with Progress(
            TextColumn("[warn]●[/warn]"),
            BarColumn(bar_width=30, style="grey37", complete_style="warn"),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("level", total=1.0)

            def on_level(level):
                progress.update(task, completed=level)

            saved_path, seconds = recorder.record_until_enter(rec_path, on_level=on_level)
    except Exception as exc:
        error(t(lang, "recording_device_error", error=str(exc)))
        return

    success(t(lang, "recording_stopped", seconds=seconds))
    success(t(lang, "recording_saved", path=str(saved_path)))

    model_size = pick_model(lang, config["default_model"])
    source_lang = pick_source_lang(lang, config["default_source_lang"])
    output_dir = Path(config["default_output_dir"]).expanduser()
    run_transcription(lang, saved_path, model_size, source_lang, output_dir, config)


def handle_batch(lang: str, config: dict):
    rule(t(lang, "menu_batch"))
    folder_str = questionary.path(
        t(lang, "batch_folder_prompt"), only_directories=True, style=QSTYLE
    ).ask()
    if not folder_str:
        return
    folder = Path(folder_str).expanduser()
    if not folder.is_dir():
        error(t(lang, "folder_not_found", path=folder_str))
        return

    files = sorted(
        p for p in folder.iterdir()
        if p.is_file() and transcriber.is_supported_file(str(p))
    )
    if not files:
        warn(t(lang, "batch_no_files"))
        return

    success(t(lang, "batch_found", count=len(files)))
    model_size = pick_model(lang, config["default_model"])
    source_lang = pick_source_lang(lang, config["default_source_lang"])
    output_dir = Path(config["default_output_dir"]).expanduser()

    ok, failed = 0, 0
    for i, f in enumerate(files, start=1):
        console.print()
        rule(t(lang, "batch_processing", index=i, total=len(files), name=f.name))
        result = run_transcription(lang, f, model_size, source_lang, output_dir, config)
        ok += int(result)
        failed += int(not result)

    console.print()
    rule(t(lang, "batch_summary_title"))
    success(t(lang, "batch_done", ok=ok, failed=failed))


def handle_history(lang: str):
    rule(t(lang, "menu_history"))
    entries = storage.load_history()
    if not entries:
        warn(t(lang, "history_empty"))
        return

    table = Table(show_lines=False, header_style="accent")
    table.add_column(t(lang, "history_col_date"))
    table.add_column(t(lang, "history_col_file"))
    table.add_column(t(lang, "history_col_lang"))
    table.add_column(t(lang, "history_col_model"))
    table.add_column(t(lang, "history_col_duration"), justify="right")
    table.add_column(t(lang, "history_col_words"), justify="right")

    for e in entries[-50:]:
        table.add_row(
            e.get("timestamp", "")[:19].replace("T", " "),
            Path(e.get("source_file", "?")).name,
            e.get("language", "?"),
            e.get("model", "?"),
            human_seconds(e.get("duration_seconds", 0)),
            str(e.get("word_count", "?")),
        )
    console.print(table)

    if questionary.confirm(t(lang, "history_clear_confirm"), default=False, style=QSTYLE).ask():
        storage.clear_history()
        success(t(lang, "history_cleared"))


def handle_settings(lang: str, config: dict):
    while True:
        rule(t(lang, "settings_title"))
        kv(t(lang, "settings_default_model"), config["default_model"])
        kv(t(lang, "settings_default_source_lang"), config["default_source_lang"])
        kv(t(lang, "settings_default_output_dir"), config["default_output_dir"])
        kv(t(lang, "settings_ui_language"), config["ui_language"])
        console.print()

        choice = questionary.select(
            t(lang, "settings_change"),
            choices=[
                Choice(title=t(lang, "settings_default_model"), value="model"),
                Choice(title=t(lang, "settings_default_source_lang"), value="src_lang"),
                Choice(title=t(lang, "settings_default_output_dir"), value="out_dir"),
                Choice(title=t(lang, "settings_ui_language"), value="ui_lang"),
                Choice(title=t(lang, "settings_back"), value="back"),
            ],
            style=QSTYLE,
        ).ask()

        if choice in (None, "back"):
            return
        if choice == "model":
            config["default_model"] = pick_model(lang, config["default_model"])
        elif choice == "src_lang":
            config["default_source_lang"] = pick_source_lang(lang, config["default_source_lang"])
        elif choice == "out_dir":
            new_dir = questionary.path(t(lang, "settings_enter_output_dir"), style=QSTYLE).ask()
            if new_dir:
                config["default_output_dir"] = str(Path(new_dir).expanduser())
        elif choice == "ui_lang":
            new_lang = questionary.select(
                t(lang, "select_language_prompt"),
                choices=[Choice(title="English", value="en"), Choice(title="فارسی", value="fa")],
                style=QSTYLE,
            ).ask()
            if new_lang:
                lang = new_lang
                config["ui_language"] = new_lang

        storage.save_config(config)
        success(t(lang, "settings_saved"))
        console.print()


def handle_help(lang: str):
    rule(t(lang, "help_title"))
    console.print(Panel(t(lang, "help_body"), border_style="accent"))
    info(t(lang, "help_repo"))
    console.print()
    info(t(lang, "ffmpeg_note"))


# --------------------------------------------------------------------------
# Main menu loop
# --------------------------------------------------------------------------

def main_menu(lang: str, config: dict):
    while True:
        console.print()
        rule(t(lang, "main_menu_title"))
        choice = questionary.select(
            t(lang, "main_menu_title"),
            choices=[
                Choice(title=t(lang, "menu_transcribe_file"), value="file"),
                Choice(title=t(lang, "menu_record"), value="record"),
                Choice(title=t(lang, "menu_batch"), value="batch"),
                Choice(title=t(lang, "menu_history"), value="history"),
                Choice(title=t(lang, "menu_settings"), value="settings"),
                Choice(title=t(lang, "menu_help"), value="help"),
                Choice(title=t(lang, "menu_exit"), value="exit"),
            ],
            style=QSTYLE,
        ).ask()

        if choice in (None, "exit"):
            if questionary.confirm(t(lang, "confirm_exit"), default=True, style=QSTYLE).ask():
                console.print()
                success(t(lang, "goodbye"))
                return
            continue

        try:
            if choice == "file":
                handle_transcribe_file(lang, config)
            elif choice == "record":
                handle_record(lang, config)
            elif choice == "batch":
                handle_batch(lang, config)
            elif choice == "history":
                handle_history(lang)
            elif choice == "settings":
                handle_settings(lang, config)
            elif choice == "help":
                handle_help(lang)
        except KeyboardInterrupt:
            console.print()
            warn(t(lang, "cancelled"))
        except Exception as exc:
            error(t(lang, "error_generic", error=str(exc)))


# --------------------------------------------------------------------------
# Non-interactive (scriptable) mode
# --------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Voice to Text — offline speech transcription (Whisper-based)."
    )
    parser.add_argument("--file", help="Audio/video file to transcribe (skips the menu).")
    parser.add_argument("--model", choices=MODEL_SIZES, help="Whisper model size.")
    parser.add_argument("--source-lang", dest="source_lang",
                         help="Audio language code, or 'auto' (default).")
    parser.add_argument("--formats", default="txt",
                         help="Comma-separated export formats: txt,srt,vtt,json")
    parser.add_argument("--output-dir", dest="output_dir", help="Where to save the output(s).")
    parser.add_argument("--ui-lang", dest="ui_lang", choices=["en", "fa"],
                         help="Interface language for this run.")
    return parser


def run_cli_mode(args, config: dict):
    lang = args.ui_lang or config.get("ui_language") or "en"
    print_banner(t(lang, "app_subtitle"))
    audio_path = Path(args.file).expanduser()
    model_size = args.model or config["default_model"]
    source_lang = args.source_lang or config["default_source_lang"]
    output_dir = Path(args.output_dir).expanduser() if args.output_dir else Path(config["default_output_dir"]).expanduser()

    # Monkey-patch the format picker for non-interactive mode.
    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
    global pick_export_formats
    pick_export_formats = lambda _lang: formats  # noqa: E731

    ok = run_transcription(lang, audio_path, model_size, source_lang, output_dir, config)
    sys.exit(0 if ok else 1)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main():
    parser = build_arg_parser()
    args = parser.parse_args()
    config = storage.load_config()

    if args.file:
        run_cli_mode(args, config)
        return

    lang = choose_ui_language(config)
    print_banner(t(lang, "app_subtitle"))
    success(t(lang, "welcome"))

    if shutil.which("ffmpeg") is None:
        info(t(lang, "ffmpeg_note"))

    try:
        main_menu(lang, config)
    except KeyboardInterrupt:
        console.print()
        warn(t(lang, "cancelled"))


if __name__ == "__main__":
    main()
