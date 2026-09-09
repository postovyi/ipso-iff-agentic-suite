import csv
import io
from datetime import datetime, timedelta, timezone

import pytest

from checkpoint import load_checkpoint
from scraper import process_channel


class FakeMessage:
    def __init__(self, message_id, date, text=None, caption=None):
        self.id = message_id
        self.date = date
        self.text = text
        self.caption = caption


class FakeClient:
    """Stands in for pyrogram.Client. history maps username -> list[FakeMessage]
    ordered newest-first, matching real get_chat_history order."""

    def __init__(self, history: dict[str, list[FakeMessage]]):
        self.history = history

    async def get_chat_history(self, username, offset_id=0):
        messages = self.history[username]
        for m in messages:
            if offset_id and m.id >= offset_id:
                continue
            yield m


NOW = datetime(2026, 8, 30, tzinfo=timezone.utc)
CUTOFF = NOW - timedelta(days=7)

LONG_POST_1 = "a valid post that is at least fifty characters long here"
LONG_POST_2 = "first valid post that is at least fifty characters long"
LONG_POST_3 = "second valid post that is at least fifty characters long"
LONG_POST_4 = "already processed earlier run, well over fifty characters"
LONG_POST_5 = "should be picked up on resume, well over fifty characters"
LONG_POST_6 = "also picked up on resume run, well over fifty characters"


def make_writer():
    buf = io.StringIO()
    writer = csv.writer(buf)
    return buf, writer


@pytest.mark.asyncio
async def test_process_channel_writes_valid_posts_within_window(tmp_path):
    messages = [
        FakeMessage(3, NOW - timedelta(days=1), text=LONG_POST_1),
        FakeMessage(2, NOW - timedelta(days=2), text="too short"),  # < 50 chars, skipped
        FakeMessage(1, NOW - timedelta(days=10), text="too old to include here, well over fifty characters long"),
    ]
    client = FakeClient({"testchan": messages})
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint = {}
    buf, writer = make_writer()

    await process_channel(
        client, "testchan", "normal", CUTOFF, writer, checkpoint, checkpoint_path
    )

    rows = buf.getvalue().splitlines()
    assert len(rows) == 1
    assert LONG_POST_1 in rows[0]
    assert rows[0].endswith("testchan,normal")
    assert checkpoint["testchan"]["status"] == "done"


@pytest.mark.asyncio
async def test_process_channel_persists_checkpoint_after_every_message(tmp_path):
    messages = [
        FakeMessage(2, NOW - timedelta(days=1), text=LONG_POST_2),
        FakeMessage(1, NOW - timedelta(days=2), text=LONG_POST_3),
    ]
    client = FakeClient({"testchan": messages})
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint = {}
    buf, writer = make_writer()

    await process_channel(
        client, "testchan", "normal", CUTOFF, writer, checkpoint, checkpoint_path
    )

    on_disk = load_checkpoint(checkpoint_path)
    assert on_disk["testchan"]["status"] == "done"


@pytest.mark.asyncio
async def test_process_channel_resumes_from_last_message_id(tmp_path):
    messages = [
        FakeMessage(3, NOW - timedelta(days=1), text=LONG_POST_4),
        FakeMessage(2, NOW - timedelta(days=2), text=LONG_POST_5),
        FakeMessage(1, NOW - timedelta(days=3), text=LONG_POST_6),
    ]
    client = FakeClient({"testchan": messages})
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint = {"testchan": {"status": "in_progress", "last_message_id": 3}}
    buf, writer = make_writer()

    await process_channel(
        client, "testchan", "normal", CUTOFF, writer, checkpoint, checkpoint_path
    )

    rows = buf.getvalue().splitlines()
    assert len(rows) == 2
    assert LONG_POST_4 not in buf.getvalue()
    assert checkpoint["testchan"]["status"] == "done"


@pytest.mark.asyncio
async def test_process_channel_skips_already_done(tmp_path):
    client = FakeClient(
        {"testchan": [FakeMessage(1, NOW, text="should not be fetched at all, over fifty chars")]}
    )
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint = {"testchan": {"status": "done"}}
    buf, writer = make_writer()

    await process_channel(
        client, "testchan", "normal", CUTOFF, writer, checkpoint, checkpoint_path
    )

    assert buf.getvalue() == ""


@pytest.mark.asyncio
async def test_process_channel_skips_boilerplate_siren_post(tmp_path):
    siren_text = (
        "🟡 Бучанський район - відбій повітряної тривоги!\n\n"
        "Зверніть увагу, повітряна тривога досі триває у:\n- Обухівський район"
    )
    messages = [FakeMessage(1, NOW - timedelta(days=1), text=siren_text)]
    client = FakeClient({"testchan": messages})
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint = {}
    buf, writer = make_writer()

    await process_channel(
        client, "testchan", "normal", CUTOFF, writer, checkpoint, checkpoint_path
    )

    assert buf.getvalue() == ""
    assert checkpoint["testchan"]["status"] == "done"


@pytest.mark.asyncio
async def test_process_channel_writes_category_from_argument(tmp_path):
    messages = [FakeMessage(1, NOW - timedelta(days=1), text=LONG_POST_1)]
    client = FakeClient({"testchan": messages})
    checkpoint_path = tmp_path / "checkpoint.json"
    checkpoint = {}
    buf, writer = make_writer()

    await process_channel(
        client, "testchan", "pro_russian", CUTOFF, writer, checkpoint, checkpoint_path
    )

    rows = list(csv.reader(io.StringIO(buf.getvalue())))
    assert rows[0][4] == "pro_russian"
