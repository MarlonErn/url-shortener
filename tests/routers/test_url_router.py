# Test if duplicated URL returns same short_code
def test_duplicate_url_returns_existing_short_code(client):
    testing_url = "https://router-test.com/page-a"
    payload = {"original_url": testing_url}

    first = client.post("/shorten", json=payload)
    second = client.post("/shorten", json=payload)

    assert first.status_code == 201, "Duplicated URL founded. Must be a new short_code for a new original URL"
    assert second.status_code == 200, "New short_code created. Must be a duplicated original URL and return a short_code already existent"

    first_body = first.json()
    second_body = second.json()

    assert first_body["short_code"] == second_body["short_code"], "New short_code generated for same original_url"
    assert first_body["original_url"] == second_body["original_url"], "original_url returned is not the same as sended at the POST"


# Test redirecting and click-counter
def test_url_redirection_and_click_counter(client):
    testing_url = "https://router-test.com/page-b"
    payload = {"original_url": testing_url}

    url_recorded = client.post("/shorten", json=payload)
    short_code = url_recorded.json()['short_code']

    # Test if counter starts at zero
    first_stats = client.get(f"/{short_code}/stats")
    assert first_stats.status_code == 200, "Stats could not be found"
    assert first_stats.json()['clicks'] == 0, "Click-counter is not starting at 0 (zero)"

    # Test if redirection is working
    redirection_test = client.get(f"/{short_code}", follow_redirects=False)
    assert redirection_test.status_code == 302, "Redirection has not worked"
    assert redirection_test.headers['location'] == testing_url, "Redirected to wrong URL"

    # Test if click-counter changed
    second_stats = client.get(f"/{short_code}/stats")
    assert second_stats.status_code == 200, "Stats could not be found"
    assert second_stats.json()['clicks'] == first_stats.json()['clicks']+1, "Click-counter did not increased value at stats"


# Test wrong short_code
def test_nonexistent_short_code_returns_404(client):
    wrong_short_code = "zz"

    # Test redirection for wrong short_code
    redirection_test = client.get(f"/{wrong_short_code}", follow_redirects=False)
    assert redirection_test.status_code == 404, "Short code does not exist, but the request was redirected."
    assert redirection_test.json() == {"detail": "Short URL not found"}, "Returned JSON incorrect"

    # Test stats for wrong short_code
    stats_test = client.get(f"/{wrong_short_code}/stats")
    assert stats_test.status_code == 404, "Short code does not exist, but stats were returned."
    assert stats_test.json() == {"detail": "Short URL not found"}, "Returned JSON incorrect"