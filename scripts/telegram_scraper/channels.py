import json
from pathlib import Path


def load_channels(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def usernames(channels: list[dict]) -> list[str]:
    return [c["username"] for c in channels]


CATEGORY_GROUPS = {
    "pro_russian": "pro_russian",
    "official_media_editions": "ground_truth",
    "bloggers": "normal",
}


def category_group(category: str) -> str:
    return CATEGORY_GROUPS[category]


def scrapable_channels(channels: list[dict]) -> list[dict]:
    return [c for c in channels if c["category"] in CATEGORY_GROUPS]
