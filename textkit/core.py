"""Чистые функции обработки текста — без зависимости от веб-фреймворка."""

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass

_TRANSLIT = str.maketrans(
    {
        "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
        "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
        "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
        "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
        "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    }
)  # fmt: skip

_WORD_RE = re.compile(r"\w+", re.UNICODE)


@dataclass(frozen=True)
class TextStats:
    characters: int
    words: int
    lines: int
    top_words: list[tuple[str, int]]


def slugify(text: str, max_length: int = 80) -> str:
    """Превращает произвольный текст (в том числе кириллицу) в URL-slug."""
    text = text.lower().translate(_TRANSLIT)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:max_length].rstrip("-")


def text_stats(text: str, top: int = 5) -> TextStats:
    words = [w.lower() for w in _WORD_RE.findall(text)]
    return TextStats(
        characters=len(text),
        words=len(words),
        lines=len(text.splitlines()) if text else 0,
        top_words=Counter(words).most_common(top),
    )
