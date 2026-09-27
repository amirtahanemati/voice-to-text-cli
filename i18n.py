# -*- coding: utf-8 -*-
"""
i18n.py
Bilingual (English / Persian) text strings for the Voice-to-Text CLI.

Add a new language by adding a new top-level key to STRINGS and making
sure every key that exists in STRINGS["en"] also exists there (missing
keys silently fall back to English).
"""

STRINGS = {
    "en": {
        "app_title": "VOICE TO TEXT",
        "app_subtitle": "A terminal transcription studio, powered by Whisper",
        "select_language_prompt": "Choose your language",
        "lang_choice_en": "English",
        "lang_choice_fa": "فارسی (Persian)",
        "welcome": "Welcome! Let's turn some audio into text.",
        "main_menu_title": "Main Menu",
        "menu_transcribe_file": "Transcribe an audio file",
        "menu_record": "Record from microphone & transcribe",
        "menu_batch": "Batch-transcribe a whole folder",
        "menu_history": "View transcription history",
        "menu_settings": "Settings",
        "menu_help": "Help / About",
        "menu_exit": "Exit",
        "goodbye": "Goodbye! Thanks for using Voice to Text.",
        "confirm_exit": "Are you sure you want to exit?",

        "choose_model_prompt": "Choose a Whisper model size",
        "model_tiny": "tiny      – fastest, lowest accuracy",
        "model_base": "base      – fast, decent accuracy",
        "model_small": "small     – balanced (recommended)",
        "model_medium": "medium    – slower, high accuracy",
        "model_large": "large-v3  – slowest, best accuracy",

        "choose_source_lang_prompt": "Audio language",
        "lang_auto": "Auto-detect",
        "lang_english": "English",
        "lang_persian": "Persian (Farsi)",
        "lang_other": "Other (type a language code)",
        "enter_lang_code_prompt": "Enter an ISO language code (e.g. de, fr, ar)",

        "file_path_prompt": "Path to the audio/video file",
        "file_not_found": "File not found: {path}",
        "unsupported_file": "That doesn't look like an audio/video file: {path}",

        "loading_model": "Loading '{model}' model (first run downloads it, please wait)...",
        "model_ready": "Model ready.",
        "detecting_language": "Detecting language...",
        "detected_language": "Detected language: {lang} (confidence {prob:.0%})",
        "transcribing_label": "Transcribing",
        "transcription_done": "Transcription complete!",

        "stats_title": "Summary",
        "stats_duration": "Audio duration",
        "stats_words": "Word count",
        "stats_elapsed": "Time taken",
        "stats_speed": "Speed",
        "stats_output": "Saved to",

        "ask_more_formats": "Also export as:",
        "format_txt": "Plain text (.txt)",
        "format_srt": "Subtitles (.srt)",
        "format_vtt": "WebVTT (.vtt)",
        "format_json": "Raw segments + metadata (.json)",

        "copy_clipboard_prompt": "Copy the transcript to your clipboard?",
        "copied_clipboard": "Copied to clipboard.",
        "clipboard_unavailable": "Clipboard support isn't available (install 'pyperclip').",

        "live_preview_title": "Live transcript",
        "press_enter_continue": "Press Enter to continue...",

        "record_instructions": "Press ENTER to start recording, then ENTER again to stop.",
        "recording_started": "Recording... press ENTER to stop.",
        "recording_stopped": "Recording stopped ({seconds:.1f}s captured).",
        "recording_saved": "Recording saved to {path}",
        "recording_device_error": "Could not access the microphone: {error}",
        "recording_unavailable": "Microphone recording isn't available (install 'sounddevice' and 'soundfile').",

        "batch_folder_prompt": "Path to the folder to batch-transcribe",
        "folder_not_found": "Folder not found: {path}",
        "batch_no_files": "No audio/video files found in that folder.",
        "batch_found": "Found {count} file(s) to transcribe.",
        "batch_processing": "[{index}/{total}] {name}",
        "batch_summary_title": "Batch summary",
        "batch_done": "Batch finished: {ok} succeeded, {failed} failed.",

        "history_title": "Transcription History",
        "history_empty": "No transcriptions yet — go make some!",
        "history_col_date": "Date",
        "history_col_file": "Source",
        "history_col_lang": "Lang",
        "history_col_model": "Model",
        "history_col_duration": "Duration",
        "history_col_words": "Words",
        "history_view_prompt": "Select an entry to view (or go back)",
        "history_back": "‹ Back",
        "history_open_output": "Open output file location: {path}",
        "history_cleared": "History cleared.",
        "history_clear_confirm": "Clear all history? This cannot be undone.",
        "history_clear_action": "Clear history",

        "settings_title": "Settings",
        "settings_default_model": "Default model size",
        "settings_default_source_lang": "Default audio language",
        "settings_default_output_dir": "Default output folder",
        "settings_ui_language": "Interface language",
        "settings_change": "Change a setting",
        "settings_back": "‹ Back to main menu",
        "settings_saved": "Settings saved.",
        "settings_current": "Current settings",
        "settings_enter_output_dir": "Enter a folder path for saved transcripts",

        "help_title": "Help & About",
        "help_body": (
            "Voice to Text turns speech in audio/video files (or your microphone)\n"
            "into text, subtitles, or structured data — fully offline, using\n"
            "OpenAI's Whisper model via faster-whisper.\n\n"
            "Features:\n"
            "  • Transcribe single files or whole folders in batch\n"
            "  • Record straight from your microphone\n"
            "  • Auto language detection or manual selection\n"
            "  • Export to .txt, .srt, .vtt, or .json\n"
            "  • Live transcript preview while it works\n"
            "  • Local history of everything you've transcribed\n"
            "  • Bilingual interface: English / Persian\n\n"
            "Tip: run with --help to see command-line flags for scripting."
        ),
        "help_repo": "Original project: github.com/amirtahanemati/voice-to-text",

        "error_generic": "Something went wrong: {error}",
        "ffmpeg_note": (
            "Note: decoding is handled internally (PyAV), so a separate ffmpeg\n"
            "install usually isn't required. If a file fails to load, installing\n"
            "ffmpeg system-wide can help."
        ),
        "no_gpu": "No GPU detected — running on CPU (this can be slower for larger models).",
        "gpu_found": "GPU detected — using CUDA for faster transcription.",
        "cancelled": "Cancelled.",
    },

    "fa": {
        "app_title": "تبدیل صدا به متن",
        "app_subtitle": "استودیوی رونویسی ترمینالی، بر پایه‌ی Whisper",
        "select_language_prompt": "زبان خود را انتخاب کنید",
        "lang_choice_en": "English",
        "lang_choice_fa": "فارسی",
        "welcome": "خوش آمدید! بیایید صدا را به متن تبدیل کنیم.",
        "main_menu_title": "منوی اصلی",
        "menu_transcribe_file": "رونویسی یک فایل صوتی",
        "menu_record": "ضبط از میکروفون و رونویسی",
        "menu_batch": "رونویسی گروهی یک پوشه",
        "menu_history": "مشاهده‌ی تاریخچه‌ی رونویسی‌ها",
        "menu_settings": "تنظیمات",
        "menu_help": "راهنما / درباره",
        "menu_exit": "خروج",
        "goodbye": "خداحافظ! ممنون که از این برنامه استفاده کردید.",
        "confirm_exit": "مطمئن هستید می‌خواهید خارج شوید؟",

        "choose_model_prompt": "اندازه‌ی مدل Whisper را انتخاب کنید",
        "model_tiny": "tiny      – سریع‌ترین، دقت کمتر",
        "model_base": "base      – سریع، دقت مناسب",
        "model_small": "small     – متعادل (پیشنهادی)",
        "model_medium": "medium    – کندتر، دقت بالا",
        "model_large": "large-v3  – کندترین، بهترین دقت",

        "choose_source_lang_prompt": "زبان فایل صوتی",
        "lang_auto": "تشخیص خودکار",
        "lang_english": "انگلیسی",
        "lang_persian": "فارسی",
        "lang_other": "زبان دیگر (کد زبان را وارد کنید)",
        "enter_lang_code_prompt": "کد زبان را وارد کنید (مثلاً de، fr، ar)",

        "file_path_prompt": "مسیر فایل صوتی/تصویری",
        "file_not_found": "فایل پیدا نشد: {path}",
        "unsupported_file": "این یک فایل صوتی/تصویری معتبر به نظر نمی‌رسد: {path}",

        "loading_model": "در حال بارگذاری مدل «{model}» (اجرای اول دانلود می‌شود، کمی صبر کنید)...",
        "model_ready": "مدل آماده است.",
        "detecting_language": "در حال تشخیص زبان...",
        "detected_language": "زبان تشخیص داده‌شده: {lang} (اطمینان {prob:.0%})",
        "transcribing_label": "در حال رونویسی",
        "transcription_done": "رونویسی کامل شد!",

        "stats_title": "خلاصه",
        "stats_duration": "مدت زمان صدا",
        "stats_words": "تعداد کلمات",
        "stats_elapsed": "زمان صرف‌شده",
        "stats_speed": "سرعت",
        "stats_output": "ذخیره شد در",

        "ask_more_formats": "همچنین خروجی بگیر به صورت:",
        "format_txt": "متن ساده (.txt)",
        "format_srt": "زیرنویس (.srt)",
        "format_vtt": "وب‌وی‌تی‌تی (.vtt)",
        "format_json": "بخش‌های خام + فراداده (.json)",

        "copy_clipboard_prompt": "متن رونویسی‌شده در کلیپ‌بورد کپی شود؟",
        "copied_clipboard": "در کلیپ‌بورد کپی شد.",
        "clipboard_unavailable": "قابلیت کلیپ‌بورد در دسترس نیست (کتابخانه‌ی 'pyperclip' را نصب کنید).",

        "live_preview_title": "پیش‌نمایش زنده‌ی متن",
        "press_enter_continue": "برای ادامه Enter را بزنید...",

        "record_instructions": "برای شروع ضبط Enter را بزنید، سپس دوباره Enter برای توقف.",
        "recording_started": "در حال ضبط... برای توقف Enter را بزنید.",
        "recording_stopped": "ضبط متوقف شد ({seconds:.1f} ثانیه ضبط شد).",
        "recording_saved": "فایل ضبط‌شده ذخیره شد در {path}",
        "recording_device_error": "دسترسی به میکروفون ممکن نشد: {error}",
        "recording_unavailable": "ضبط از میکروفون در دسترس نیست (کتابخانه‌های 'sounddevice' و 'soundfile' را نصب کنید).",

        "batch_folder_prompt": "مسیر پوشه برای رونویسی گروهی",
        "folder_not_found": "پوشه پیدا نشد: {path}",
        "batch_no_files": "هیچ فایل صوتی/تصویری در این پوشه پیدا نشد.",
        "batch_found": "{count} فایل برای رونویسی پیدا شد.",
        "batch_processing": "[{index}/{total}] {name}",
        "batch_summary_title": "خلاصه‌ی رونویسی گروهی",
        "batch_done": "رونویسی گروهی تمام شد: {ok} موفق، {failed} ناموفق.",

        "history_title": "تاریخچه‌ی رونویسی‌ها",
        "history_empty": "هنوز هیچ رونویسی‌ای انجام نشده — یکی بسازید!",
        "history_col_date": "تاریخ",
        "history_col_file": "منبع",
        "history_col_lang": "زبان",
        "history_col_model": "مدل",
        "history_col_duration": "مدت زمان",
        "history_col_words": "کلمات",
        "history_view_prompt": "یک مورد را برای مشاهده انتخاب کنید (یا بازگشت)",
        "history_back": "‹ بازگشت",
        "history_open_output": "مسیر فایل خروجی: {path}",
        "history_cleared": "تاریخچه پاک شد.",
        "history_clear_confirm": "تمام تاریخچه پاک شود؟ این کار قابل بازگشت نیست.",
        "history_clear_action": "پاک‌کردن تاریخچه",

        "settings_title": "تنظیمات",
        "settings_default_model": "اندازه‌ی مدل پیش‌فرض",
        "settings_default_source_lang": "زبان پیش‌فرض صدا",
        "settings_default_output_dir": "پوشه‌ی خروجی پیش‌فرض",
        "settings_ui_language": "زبان رابط کاربری",
        "settings_change": "تغییر یک تنظیم",
        "settings_back": "‹ بازگشت به منوی اصلی",
        "settings_saved": "تنظیمات ذخیره شد.",
        "settings_current": "تنظیمات فعلی",
        "settings_enter_output_dir": "مسیر پوشه‌ای برای ذخیره‌ی رونویسی‌ها وارد کنید",

        "help_title": "راهنما و درباره",
        "help_body": (
            "این برنامه گفتار موجود در فایل‌های صوتی/تصویری (یا میکروفون شما) را\n"
            "به‌طور کاملاً آفلاین، با استفاده از مدل Whisper شرکت OpenAI (از طریق\n"
            "faster-whisper) به متن، زیرنویس یا داده‌ی ساخت‌یافته تبدیل می‌کند.\n\n"
            "امکانات:\n"
            "  • رونویسی تک‌فایل یا رونویسی گروهی یک پوشه کامل\n"
            "  • ضبط مستقیم از میکروفون\n"
            "  • تشخیص خودکار زبان یا انتخاب دستی\n"
            "  • خروجی به فرمت‌های .txt، .srt، .vtt یا .json\n"
            "  • پیش‌نمایش زنده‌ی متن حین پردازش\n"
            "  • تاریخچه‌ی محلی از همه‌ی رونویسی‌های قبلی\n"
            "  • رابط کاربری دوزبانه: انگلیسی / فارسی\n\n"
            "نکته: برای دیدن پرچم‌های خط فرمان، با --help اجرا کنید."
        ),
        "help_repo": "پروژه‌ی اصلی: github.com/amirtahanemati/voice-to-text",

        "error_generic": "مشکلی پیش آمد: {error}",
        "ffmpeg_note": (
            "نکته: رمزگشایی صدا به‌صورت داخلی (PyAV) انجام می‌شود، پس معمولاً نیازی\n"
            "به نصب جداگانه‌ی ffmpeg نیست. اگر فایلی بارگذاری نشد، نصب ffmpeg روی\n"
            "سیستم می‌تواند کمک کند."
        ),
        "no_gpu": "کارت گرافیک پیدا نشد — روی CPU اجرا می‌شود (برای مدل‌های بزرگ‌تر ممکن است کندتر باشد).",
        "gpu_found": "کارت گرافیک پیدا شد — از CUDA برای رونویسی سریع‌تر استفاده می‌شود.",
        "cancelled": "لغو شد.",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    """Look up a translated string, falling back to English, then the key itself."""
    table = STRINGS.get(lang, STRINGS["en"])
    template = table.get(key, STRINGS["en"].get(key, key))
    return template.format(**kwargs) if kwargs else template
