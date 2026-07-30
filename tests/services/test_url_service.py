from app.services.url_service import create_short_url


# Testing if short_code is generating correctly
def test_create_short_url_generates_short_code(db_session):
    result = create_short_url(db_session, "https://exemplo.com/pagina-a")

    assert result.short_code is not None, "Short code cannot be generated"
    assert len(result.short_code) > 0, "Short code length equals 0"


# Test if original_url is saved correctly
def test_create_short_url_persists_original_url(db_session):
    original = "https://exemplo.com/pagina-b"

    result = create_short_url(db_session, original)

    assert result.original_url == original, "Original url is different then text assigned at function"


# Test if counter starts at 0
def test_create_short_url_starts_with_zero_clicks(db_session):
    result = create_short_url(db_session, "https://exemplo.com/pagina-c")

    assert result.clicks == 0, "Start click-counter is not starting in 0"


# Test if autoincrement is working
def test_create_short_url_increments_id_across_calls(db_session):
    first = create_short_url(db_session, "https://exemplo.com/pagina-d")
    second = create_short_url(db_session, "https://exemplo.com/pagina-e")

    assert second.id > first.id, "ID is not incrementing after include"