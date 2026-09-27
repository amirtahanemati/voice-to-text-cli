# -*- coding: utf-8 -*-
"""
ui.py
Shared rich Console, theme, banner and small display helpers.
"""
from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich.rule import Rule

THEME = Theme({
    "brand": "bold magenta",
    "accent": "bold cyan",
    "ok": "bold green",
    "warn": "bold yellow",
    "err": "bold red",
    "muted": "dim white",
    "value": "bold white",
})

console = Console(theme=THEME, highlight=False)

_BANNER = r"""
 __      __    _              _        _____         _
 \ \    / /   (_)            | |      |_   _|       | |
  \ \  / /__   _   ___  ___  | |_ ___    | |   ___   | |_   ___  __  __ _
   \ \/ / _ \ | | / __|/ _ \ | __/ _ \   | |  / _ \  | __| / _ \ \ \/ /| |_
    \  / (_) || || (__|  __/ | || (_) | _| |_| (_) | | |_ |  __/  >  < |  _|
     \/ \___/ |_| \___|\___|  \__\___/ |_____|\___/   \__| \___| /_/\_\|_|
"""


def print_banner(subtitle: str = "") -> None:
    console.print(Align.center(Text(_BANNER, style="brand")))
    if subtitle:
        console.print(Align.center(Text(subtitle, style="muted")))
    console.print()


def rule(title: str = "") -> None:
    console.rule(f"[accent]{title}[/accent]" if title else "")


def panel(body: str, title: str = "", style: str = "accent") -> None:
    console.print(Panel.fit(body, title=title, border_style=style))


def success(msg: str) -> None:
    console.print(f"[ok]✔[/ok] {msg}")


def warn(msg: str) -> None:
    console.print(f"[warn]⚠[/warn] {msg}")


def error(msg: str) -> None:
    console.print(f"[err]✘[/err] {msg}")


def info(msg: str) -> None:
    console.print(f"[accent]›[/accent] {msg}")


def kv(label: str, value: str) -> None:
    console.print(f"  [muted]{label}:[/muted] [value]{value}[/value]")
