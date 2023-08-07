import locatieserver.client.suggest


def test_suggest() -> None:

    result = locatieserver.client.suggest("Westerein")

    assert result
    assert result.response.num_found == 141
