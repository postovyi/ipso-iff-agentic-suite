import json

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


def test_load_checkpoint_returns_empty_dict_when_file_missing(tmp_path):
    path = tmp_path / "checkpoint.json"

    assert load_checkpoint(path) == {}


def test_load_checkpoint_reads_existing_file(tmp_path):
    path = tmp_path / "checkpoint.json"
    path.write_text(json.dumps({"foo": {"status": "done"}}), encoding="utf-8")

    assert load_checkpoint(path) == {"foo": {"status": "done"}}


def test_save_checkpoint_writes_json(tmp_path):
    path = tmp_path / "checkpoint.json"

    save_checkpoint(path, {"foo": {"status": "done"}})

    assert json.loads(path.read_text(encoding="utf-8")) == {"foo": {"status": "done"}}


def test_mark_in_progress_sets_status_and_last_message_id():
    checkpoint = {}

    mark_in_progress(checkpoint, "foo", 123)

    assert checkpoint == {"foo": {"status": "in_progress", "last_message_id": 123}}


def test_mark_done_sets_status():
    checkpoint = {"foo": {"status": "in_progress", "last_message_id": 123}}

    mark_done(checkpoint, "foo")

    assert checkpoint == {"foo": {"status": "done"}}


def test_mark_failed_sets_status():
    checkpoint = {}

    mark_failed(checkpoint, "foo")

    assert checkpoint == {"foo": {"status": "failed"}}


def test_is_done_true_for_done_status():
    assert is_done({"foo": {"status": "done"}}, "foo") is True


def test_is_done_false_for_missing_or_other_status():
    assert is_done({}, "foo") is False
    assert is_done({"foo": {"status": "in_progress", "last_message_id": 1}}, "foo") is False


def test_resume_offset_returns_last_message_id_when_in_progress():
    checkpoint = {"foo": {"status": "in_progress", "last_message_id": 456}}

    assert resume_offset(checkpoint, "foo") == 456


def test_resume_offset_returns_zero_when_not_in_progress():
    assert resume_offset({}, "foo") == 0
    assert resume_offset({"foo": {"status": "done"}}, "foo") == 0


def test_all_finished_true_when_every_channel_done_or_failed():
    checkpoint = {
        "foo": {"status": "done"},
        "bar": {"status": "failed"},
    }

    assert all_finished(checkpoint, ["foo", "bar"]) is True


def test_all_finished_false_when_any_channel_incomplete():
    checkpoint = {
        "foo": {"status": "done"},
        "bar": {"status": "in_progress", "last_message_id": 1},
    }

    assert all_finished(checkpoint, ["foo", "bar"]) is False


def test_all_finished_false_when_channel_untouched():
    checkpoint = {"foo": {"status": "done"}}

    assert all_finished(checkpoint, ["foo", "bar"]) is False
