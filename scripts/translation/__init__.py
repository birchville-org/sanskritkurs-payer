"""
Sanskritkurs Payer Translation Package.
"""

from .config import (
    LOCK_FILE_PATH, API_URL, MODEL, DE_FALLBACK_ALLOWED,
    LANGUAGES, LANG_NAMES
)
from .lock import acquire_nyx_lock

__all__ = [
    "LOCK_FILE_PATH", "API_URL", "MODEL", "DE_FALLBACK_ALLOWED",
    "LANGUAGES", "LANG_NAMES", "acquire_nyx_lock"
]
