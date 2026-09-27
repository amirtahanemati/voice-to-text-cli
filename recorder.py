# -*- coding: utf-8 -*-
"""
recorder.py
Microphone recording with a live volume meter, built on sounddevice.
Fully optional: if sounddevice/soundfile/numpy aren't installed, the rest
of the app still works — the caller should check RECORDING_AVAILABLE first.
"""
import queue
import threading
import time
from pathlib import Path
from typing import Optional, Tuple

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    RECORDING_AVAILABLE = True
except (ImportError, OSError):
    RECORDING_AVAILABLE = False

SAMPLE_RATE = 16000
CHANNELS = 1


def record_until_enter(output_path: Path, on_level=None) -> Tuple[Path, float]:
    """
    Records audio from the default microphone until the user presses Enter.
    `on_level` (optional) is called repeatedly with a 0.0-1.0 RMS level so
    the caller can draw a live meter. Returns (path, seconds_recorded).
    """
    if not RECORDING_AVAILABLE:
        raise RuntimeError("sounddevice/soundfile/numpy are not installed.")

    q: "queue.Queue" = queue.Queue()
    stop_flag = threading.Event()

    def callback(indata, frames, time_info, status):
        q.put(indata.copy())
        if on_level:
            rms = float(np.sqrt(np.mean(indata.astype("float64") ** 2)))
            on_level(min(rms * 8, 1.0))  # scaled for a nicer-looking meter

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback, dtype="float32"
    )

    chunks = []
    start_time = time.time()

    def collector():
        while not stop_flag.is_set():
            try:
                chunks.append(q.get(timeout=0.1))
            except queue.Empty:
                continue

    with stream:
        collector_thread = threading.Thread(target=collector, daemon=True)
        collector_thread.start()
        input()  # blocks until user presses Enter to stop
        stop_flag.set()
        collector_thread.join(timeout=1.0)

    elapsed = time.time() - start_time
    if chunks:
        audio = np.concatenate(chunks, axis=0)
    else:
        audio = np.zeros((0, CHANNELS), dtype="float32")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(output_path), audio, SAMPLE_RATE)
    return output_path, elapsed


def list_input_devices():
    if not RECORDING_AVAILABLE:
        return []
    devices = sd.query_devices()
    return [d["name"] for d in devices if d.get("max_input_channels", 0) > 0]
