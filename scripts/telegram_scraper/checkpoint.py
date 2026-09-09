import json
from pathlib import Path


def load_checkpoint(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_checkpoint(path: Path, checkpoint: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)


def mark_in_progress(checkpoint: dict, username: str, last_message_id: int) -> None:
    checkpoint[username] = {"status": "in_progress", "last_message_id": last_message_id}


def mark_done(checkpoint: dict, username: str) -> None:
    checkpoint[username] = {"status": "done"}


def mark_failed(checkpoint: dict, username: str) -> None:
    checkpoint[username] = {"status": "failed"}


def is_done(checkpoint: dict, username: str) -> bool:
    return checkpoint.get(username, {}).get("status") == "done"


def resume_offset(checkpoint: dict, username: str) -> int:
    entry = checkpoint.get(username, {})
    if entry.get("status") == "in_progress":
        return entry.get("last_message_id", 0)
    return 0


def all_finished(checkpoint: dict, all_usernames: list[str]) -> bool:
    return all(checkpoint.get(u, {}).get("status") in ("done", "failed") for u in all_usernames)
