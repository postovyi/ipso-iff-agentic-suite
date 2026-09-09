import asyncio
import csv
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import FloodWait

from channels import category_group, load_channels, scrapable_channels, usernames
from checkpoint import (
    all_finished,
    is_done,
    load_checkpoint,
    mark_done,
    mark_failed,
    mark_in_progress,
    resume_offset,
    save_checkpoint,
)
from posts import build_row, extract_text, is_boilerplate, is_valid_text

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
CSV_PATH = OUTPUT_DIR / "posts.csv"
CHECKPOINT_PATH = OUTPUT_DIR / "checkpoint.json"
CHANNELS_PATH = BASE_DIR / "channels.json"
CHANNEL_DELAY_SECONDS = 1.5


async def process_channel(
    client, username, category, cutoff, csv_writer, checkpoint, checkpoint_path
):
    if is_done(checkpoint, username):
        return

    offset_id = resume_offset(checkpoint, username)

    async for message in client.get_chat_history(username, offset_id=offset_id):
        msg_date = message.date if message.date.tzinfo else message.date.replace(tzinfo=timezone.utc)
        if msg_date < cutoff:
            break

        text = extract_text(message.text, message.caption)
        if is_valid_text(text) and not is_boilerplate(text):
            row = build_row(username, message.id, msg_date.isoformat(), text, category)
            csv_writer.writerow(row)

        mark_in_progress(checkpoint, username, message.id)
        save_checkpoint(checkpoint_path, checkpoint)

    mark_done(checkpoint, username)
    save_checkpoint(checkpoint_path, checkpoint)


async def main():
    load_dotenv()
    api_id = os.environ["TELEGRAM_API_ID"]
    api_hash = os.environ["TELEGRAM_API_HASH"]
    session_string = os.environ["TELEGRAM_SESSION_STRING"]
    session_name = os.environ.get("TELEGRAM_SESSION_NAME", "scraper_session")

    OUTPUT_DIR.mkdir(exist_ok=True)
    channels = scrapable_channels(load_channels(CHANNELS_PATH))
    all_usernames = usernames(channels)
    categories = {c["username"]: category_group(c["category"]) for c in channels}
    checkpoint = load_checkpoint(CHECKPOINT_PATH)
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)

    write_header = not CSV_PATH.exists()

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["text", "date", "url", "channel", "category"])

        async with Client(
            session_name,
            api_id=api_id,
            api_hash=api_hash,
            session_string=session_string,
            in_memory=True,
        ) as client:
            failures = []
            for username in all_usernames:
                category = categories[username]
                try:
                    await process_channel(
                        client, username, category, cutoff, writer, checkpoint, CHECKPOINT_PATH
                    )
                except FloodWait as e:
                    print(f"FloodWait on {username}: sleeping {e.value}s", file=sys.stderr)
                    time.sleep(e.value)
                    try:
                        await process_channel(
                            client, username, category, cutoff, writer, checkpoint, CHECKPOINT_PATH
                        )
                    except Exception as retry_err:
                        print(f"Failed {username} after retry: {retry_err}", file=sys.stderr)
                        mark_failed(checkpoint, username)
                        save_checkpoint(CHECKPOINT_PATH, checkpoint)
                        failures.append(username)
                except Exception as err:
                    print(f"Failed {username}: {err}", file=sys.stderr)
                    mark_failed(checkpoint, username)
                    save_checkpoint(CHECKPOINT_PATH, checkpoint)
                    failures.append(username)

                await asyncio.sleep(CHANNEL_DELAY_SECONDS)

    succeeded = len(all_usernames) - len(failures)
    print(f"Done. {succeeded}/{len(all_usernames)} channels succeeded.")
    if failures:
        print(f"Failed channels: {', '.join(failures)}", file=sys.stderr)

    if all_finished(checkpoint, all_usernames):
        CHECKPOINT_PATH.unlink(missing_ok=True)


if __name__ == "__main__":
    asyncio.run(main())
