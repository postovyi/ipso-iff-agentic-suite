import json
from pathlib import Path

import pytest

from channels import category_group, load_channels, scrapable_channels, usernames


def test_load_channels_reads_json_list(tmp_path):
    data = [
        {"username": "foo", "category": "bloggers"},
        {"username": "bar", "category": "pro_russian"},
    ]
    path = tmp_path / "channels.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    result = load_channels(path)

    assert result == data


def test_usernames_extracts_username_field():
    channels = [
        {"username": "foo", "category": "bloggers"},
        {"username": "bar", "category": "pro_russian"},
    ]

    assert usernames(channels) == ["foo", "bar"]


def test_category_group_maps_pro_russian():
    assert category_group("pro_russian") == "pro_russian"


def test_category_group_maps_official_media_editions_to_ground_truth():
    assert category_group("official_media_editions") == "ground_truth"


def test_category_group_maps_bloggers_to_normal():
    assert category_group("bloggers") == "normal"


def test_category_group_raises_for_excluded_categories():
    with pytest.raises(KeyError):
        category_group("official_state_sources")
    with pytest.raises(KeyError):
        category_group("news_aggregators")


def test_scrapable_channels_keeps_only_known_categories():
    channels = [
        {"username": "a", "category": "pro_russian"},
        {"username": "b", "category": "official_state_sources"},
        {"username": "c", "category": "bloggers"},
        {"username": "d", "category": "news_aggregators"},
        {"username": "e", "category": "official_media_editions"},
    ]

    result = scrapable_channels(channels)

    assert usernames(result) == ["a", "c", "e"]
