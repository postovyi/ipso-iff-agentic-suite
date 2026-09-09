import re

MIN_TEXT_LENGTH = 50

SIREN_PREFIX_RE = re.compile(
    r"^[^\wа-яіїєґ]{0,5}"
    r"([А-ЯЇЄІҐ][\wіїєґ'\-\s]{0,45}[—\-:]\s*)?"
    r"(відбій\s+(повітряної\s+)?тривоги|повітряна\s+тривога|тривога\s+оголошена"
    r"|оголошено\s+(повітряну\s+)?тривогу|повітряна\s+тривога\s+триває)",
    re.IGNORECASE,
)

TRACK_PREFIX_RE = re.compile(
    r"^[^\wа-яіїєґ]{0,3}"
    r"("
    r"[🏍🛵]|"
    r"(загальна|общая|остаток|залишок)\s+по\s+мопедам|"
    r"(\d+\s+)?(управля\S*\s+)?(реактивн\S*\s+|нереактивн\S*\s+)?"
    r"(бпла|мопед\S*|бандерол\S*)\S*[^.]{0,60}?(курс\S*|повз\s+[А-ЯЇЄІҐ])|"
    r"[А-ЯЇЄІҐ][\wіїєґ'\-\s]{2,25}[:\-—]\s*"
    r"(бпла|реактивн\S*|мопед\S*|бандерол\S*|груп[аи]\s+реактивних|дрон\S*)"
    r")",
    re.IGNORECASE,
)

SHELTER_RE = re.compile(
    r"(shelters_map|прослідувати в укриття|укриття цивільного захисту|мапа укриттів|мапа укрытий)",
    re.IGNORECASE,
)

THREAT_STATUS_PREFIX_RE = re.compile(
    r"^[^\wа-яіїєґ]{0,3}"
    r"(чисто\b|загроза застосування|активність ворожої|"
    r"увага!?\s*\n?[^\wа-яіїєґ]{0,3}активність ворожої)",
    re.IGNORECASE,
)


def extract_text(text: str | None, caption: str | None) -> str | None:
    return text if text is not None else caption


def is_valid_text(text: str | None) -> bool:
    if text is None:
        return False
    return len(text.strip()) >= MIN_TEXT_LENGTH


def is_boilerplate(text: str) -> bool:
    stripped = text.strip()
    if SIREN_PREFIX_RE.match(stripped):
        return True
    if TRACK_PREFIX_RE.match(stripped):
        return True
    if SHELTER_RE.search(stripped):
        return True
    if THREAT_STATUS_PREFIX_RE.match(stripped):
        return True
    return False


def build_url(username: str, message_id: int) -> str:
    return f"https://t.me/{username}/{message_id}"


def build_row(
    username: str, message_id: int, date_iso: str, text: str, category: str
) -> tuple[str, str, str, str, str]:
    return (text.strip(), date_iso, build_url(username, message_id), username, category)
