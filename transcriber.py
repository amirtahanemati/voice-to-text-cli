# -*- coding: utf-8 -*-
"""
transcriber.py
Thin wrapper around faster-whisper that:
  - loads a model (auto-picks GPU if available)
  - streams segments back one at a time so the caller can render a real
    progress bar and a live transcript preview
  - reports whether a GPU was used

faster-whisper decodes audio internally via PyAV, so a separate ffmpeg
install usually isn't required.
"""
from dataclasses import dataclass
from typing import Callable, Iterator, List, Optional, Tuple

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False


SUPPORTED_EXTENSIONS = {
    ".mp3", ".wav", ".m4a", ".mp4", ".flac", ".ogg", ".opus",
    ".webm", ".mkv", ".mov", ".aac", ".wma",
}

MODEL_SIZES = ["tiny", "base", "small", "medium", "large-v3"]


@dataclass
class Segment:
    start: float
    end: float
    text: str

    def as_dict(self):
        return {"start": self.start, "end": self.end, "text": self.text}


@dataclass
class TranscriptionInfo:
    language: str
    language_probability: float
    duration: float
    used_gpu: bool


def gpu_available() -> bool:
    try:
        import ctranslate2
        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


def load_model(model_size: str) -> "WhisperModel":
    """Load a faster-whisper model, preferring GPU (float16) and falling
    back to CPU (int8) automatically."""
    if not FASTER_WHISPER_AVAILABLE:
        raise RuntimeError(
            "faster-whisper isn't installed. Run: pip install faster-whisper"
        )
    if gpu_available():
        try:
            return WhisperModel(model_size, device="cuda", compute_type="float16")
        except Exception:
            pass
    return WhisperModel(model_size, device="cpu", compute_type="int8")


def transcribe_stream(
    model: "WhisperModel",
    audio_path: str,
    language: Optional[str] = None,
    on_segment: Optional[Callable[[Segment, float], None]] = None,
) -> Tuple[List[Segment], TranscriptionInfo]:
    """
    Runs transcription and yields control back via on_segment(segment, progress_fraction)
    for every segment produced, so callers can update a progress bar / live preview.
    Returns the full list of segments plus summary info once done.
    """
    lang_arg = None if language in (None, "auto") else language

    segments_iter, info = model.transcribe(
        audio_path,
        language=lang_arg,
        vad_filter=True,
        beam_size=5,
    )

    collected: List[Segment] = []
    duration = max(info.duration, 0.001)

    for seg in segments_iter:
        s = Segment(start=seg.start, end=seg.end, text=seg.text)
        collected.append(s)
        if on_segment:
            progress = min(seg.end / duration, 1.0)
            on_segment(s, progress)

    result_info = TranscriptionInfo(
        language=info.language,
        language_probability=info.language_probability,
        duration=info.duration,
        used_gpu=gpu_available(),
    )
    return collected, result_info


def is_supported_file(path: str) -> bool:
    from pathlib import Path
    return Path(path).suffix.lower() in SUPPORTED_EXTENSIONS
