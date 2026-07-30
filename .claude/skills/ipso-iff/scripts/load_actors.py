import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def _bool(val):
    return str(val).strip().lower() in ("1", "true", "yes", "on")


def _int(val):
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


ACTORS = {
    "apify": {
        "enabled": _bool(os.getenv("APIFY_ENABLED")),
    },
    "web_search": {
        "actor": os.getenv("WEB_SEARCH_ACTOR"),
        "max_results": _int(os.getenv("WEB_SEARCH_MAX_RESULTS")),
        "enabled": _bool(os.getenv("WEB_SEARCH_ENABLED")),
    },
    "twitter": {
        "actor": os.getenv("TWITTER_ACTOR"),
        "max_results": _int(os.getenv("TWITTER_MAX_RESULTS")),
        "enabled": _bool(os.getenv("TWITTER_ENABLED")),
    },
    "reddit": {
        "actor": os.getenv("REDDIT_ACTOR"),
        "max_results": _int(os.getenv("REDDIT_MAX_RESULTS")),
        "enabled": _bool(os.getenv("REDDIT_ENABLED")),
    },
    "instagram": {
        "actor": os.getenv("INSTAGRAM_ACTOR"),
        "max_results": _int(os.getenv("INSTAGRAM_MAX_RESULTS")),
        "enabled": _bool(os.getenv("INSTAGRAM_ENABLED")),
    },
    "threads": {
        "actor": os.getenv("THREADS_ACTOR"),
        "max_results": _int(os.getenv("THREADS_MAX_RESULTS")),
        "enabled": _bool(os.getenv("THREADS_ENABLED")),
    },
    "telegram": {
        "actor": os.getenv("TELEGRAM_ACTOR"),
        "max_results": _int(os.getenv("TELEGRAM_MAX_RESULTS")),
        "enabled": _bool(os.getenv("TELEGRAM_ENABLED")),
    },
}


ENABLED_ACTORS = {name: cfg for name, cfg in ACTORS.items() if cfg["enabled"]}

if __name__ == "__main__":
    import json

    print(json.dumps(ENABLED_ACTORS, indent=2))
