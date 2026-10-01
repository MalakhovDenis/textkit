import os

from fastapi import FastAPI
from pydantic import BaseModel, Field

from textkit.core import slugify, text_stats

# В CI сюда подставляется git SHA коммита, из которого собран образ
__version__ = os.getenv("APP_VERSION", "dev")

app = FastAPI(title="textkit", version=__version__, description="Текстовые утилиты")


class TextIn(BaseModel):
    text: str = Field(max_length=100_000, examples=["Привет, мир! Привет!"])


class SlugOut(BaseModel):
    slug: str


class StatsOut(BaseModel):
    characters: int
    words: int
    lines: int
    top_words: list[tuple[str, int]]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.post("/slugify")
def slugify_endpoint(body: TextIn) -> SlugOut:
    return SlugOut(slug=slugify(body.text))


@app.post("/stats")
def stats_endpoint(body: TextIn) -> StatsOut:
    s = text_stats(body.text)
    return StatsOut(characters=s.characters, words=s.words, lines=s.lines, top_words=s.top_words)
