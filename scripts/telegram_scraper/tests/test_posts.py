from posts import build_row, build_url, extract_text, is_boilerplate, is_valid_text


def test_extract_text_prefers_text_over_caption():
    assert extract_text("hello", "a caption") == "hello"


def test_extract_text_falls_back_to_caption():
    assert extract_text(None, "a caption") == "a caption"


def test_extract_text_returns_none_when_both_missing():
    assert extract_text(None, None) is None


def test_is_valid_text_rejects_none():
    assert is_valid_text(None) is False


def test_is_valid_text_rejects_text_under_50_chars():
    assert is_valid_text("short caption under fifty characters") is False  # 37 chars


def test_is_valid_text_rejects_whitespace_only_long_string():
    assert is_valid_text(" " * 60) is False  # strips to empty


def test_is_valid_text_accepts_text_at_least_50_chars_stripped():
    text = "  " + ("x" * 50) + "  "
    assert is_valid_text(text) is True


def test_is_valid_text_rejects_text_of_49_chars():
    assert is_valid_text("x" * 49) is False


def test_build_url_formats_telegram_link():
    assert build_url("suspilnenews", 12345) == "https://t.me/suspilnenews/12345"


def test_build_row_strips_text_and_orders_fields():
    row = build_row(
        "uniannet", 42, "2026-08-25T14:32:00+00:00", "  hello world  ", "ground_truth"
    )

    assert row == (
        "hello world",
        "2026-08-25T14:32:00+00:00",
        "https://t.me/uniannet/42",
        "uniannet",
        "ground_truth",
    )


def test_is_boilerplate_detects_siren_all_clear_announcement():
    assert is_boilerplate("Київ — відбій повітряної тривоги.") is True


def test_is_boilerplate_detects_district_siren_announcement():
    text = "🟡 Бучанський район - відбій повітряної тривоги!\n\nЗверніть увагу, повітряна тривога досі триває у:\n- Обухівський район"
    assert is_boilerplate(text) is True


def test_is_boilerplate_detects_drone_tracking_post():
    assert is_boilerplate("🏍 Реактивний БпЛА повз Бровари курсом на Бориспіль.") is True


def test_is_boilerplate_detects_shelter_alert():
    text = (
        "‼️УВАГА! У Києві оголошена повітряна тривога!\n\n"
        "Просимо всіх терміново прослідувати в укриття цивільного захисту!\n"
        "Мапа укриттів - https://kyivcity.gov.ua/news/shelters_map/"
    )
    assert is_boilerplate(text) is True


def test_is_boilerplate_detects_chisto_all_clear():
    text = "Чисто.\n\n➡️ ПОДПИСАТЬСЯ \nПрисылайте контент в анонимный бот➡️ @Obstanovka_kyiv_bot ⬅️"
    assert is_boilerplate(text) is True


def test_is_boilerplate_detects_threat_direction_status():
    text = "☄️ Загроза застосування балістичного озброєння з південно-східного напрямку."
    assert is_boilerplate(text) is True


def test_is_boilerplate_detects_enemy_air_activity_status():
    text = (
        "⚠ Увага!\n🛫 Активність ворожої тактичної авіації на південному напрямку! \n"
        "🚀🚀Загроза застосування авіаційних засобів ураження для прифронтових областей!"
    )
    assert is_boilerplate(text) is True


def test_is_boilerplate_false_for_substantive_post_mentioning_alarm():
    text = (
        "Задовбали тривоги? Хочеться, щоб росіяни вмивалися кровʼю за кожну атаку? "
        "Хочете, щоб більше Шахедів збивали? Тоді донат — найкращий спосіб допомогти."
    )
    assert is_boilerplate(text) is False


def test_is_boilerplate_false_for_regular_news_post():
    text = (
        "Кабінет Міністрів затвердив новий порядок виплат для внутрішньо переміщених осіб, "
        "який набуде чинності з наступного місяця, повідомляє прес-служба уряду."
    )
    assert is_boilerplate(text) is False
