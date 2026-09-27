# Voice to Text — Terminal Edition

A bilingual (English / فارسی) terminal app for turning speech into text,
fully offline, built on top of [`faster-whisper`](https://github.com/SYSTRAN/faster-whisper)
(a fast reimplementation of OpenAI's Whisper).

This grew out of a small 17-line script that loaded Whisper and transcribed
one hardcoded `voice.mp3`. It's now a full interactive TUI:

- **Language picker on launch** — English or فارسی, remembered for next time
- **Arrow-key menus** (via `questionary`) and rich colored output
- **Transcribe a single file**, with drag-and-drop-style path autocomplete
- **Record straight from your microphone**, with a live level meter, then
  transcribe immediately
- **Batch-transcribe** every audio/video file in a folder in one go
- **Live transcript preview** streamed line-by-line while it works, plus a
  real progress bar (based on actual audio position, not a fake spinner)
- **Auto language detection**, or pick a language manually
- **5 model sizes** (`tiny` → `large-v3`) with plain-language trade-off hints
- **Export to `.txt`, `.srt`, `.vtt`, or `.json`** (pick any combination)
- **Local history** of everything you've transcribed (source file, model,
  duration, word count — viewable as a table, clearable on request)
- **Settings screen** to change your defaults (model, language, output
  folder, interface language) once instead of every run
- **Clipboard copy** for the finished transcript (optional)
- **GPU auto-detection** — uses CUDA automatically if available, otherwise
  falls back to a quantized CPU model
- **Scriptable / non-interactive mode** via command-line flags, for use in
  pipelines or cron jobs

## Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The microphone-recording and clipboard features are optional — the app
works fine without `sounddevice`/`soundfile`/`numpy`/`pyperclip` installed;
those menu items will just tell you they're unavailable.

> **Note on ffmpeg:** `faster-whisper` decodes audio internally (via PyAV),
> so a separate ffmpeg install usually isn't required. If a particular file
> ever fails to load, installing ffmpeg system-wide can help.

## Run

```bash
python main.py
```

You'll be asked to pick English or فارسی first, then dropped into the main
menu — everything else (model size, source language, export formats) is
chosen through simple arrow-key prompts.

### Scriptable mode

For automation, skip the menus entirely:

```bash
python main.py --file interview.mp3 --model small --source-lang auto \
    --formats txt,srt --output-dir ./out --ui-lang en
```

Run `python main.py --help` for the full flag list.

## Project layout

```
main.py          entry point — menus, flows, CLI flags
i18n.py           every user-facing string, in English and Persian
ui.py             rich console theme, banner, small print helpers
transcriber.py    faster-whisper wrapper (model loading, streamed segments)
recorder.py       optional microphone recording with a live meter
storage.py        JSON-backed settings + history, stored in ~/.voice_to_text_cli/
exporters.py      .txt / .srt / .vtt / .json writers
requirements.txt
```

Settings and history live in `~/.voice_to_text_cli/` (`config.json` and
`history.json`), separate from the app itself, so they survive upgrades.

## Original project

The idea started from [amirtahanemati/voice-to-text](https://github.com/amirtahanemati/voice-to-text).
