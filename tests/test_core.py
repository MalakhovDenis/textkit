import pytest

from textkit.core import slugify, text_stats


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello, World!", "hello-world"),
        ("Привет, мир", "privet-mir"),
        ("  --Щука и ёж--  ", "schuka-i-ezh"),
        ("Café déjà vu", "cafe-deja-vu"),
        ("!!!", ""),
    ],
)
def test_slugify(text: str, expected: str) -> None:
    assert slugify(text) == expected


def test_slugify_max_length_does_not_end_with_dash() -> None:
    assert slugify("aaaa bbbb", max_length=5) == "aaaa"


def test_text_stats() -> None:
    s = text_stats("Привет, мир!\nПривет!")
    assert s.words == 3
    assert s.lines == 2
    assert s.top_words[0] == ("привет", 2)


def test_text_stats_empty() -> None:
    s = text_stats("")
    assert (s.characters, s.words, s.lines, s.top_words) == (0, 0, 0, [])
