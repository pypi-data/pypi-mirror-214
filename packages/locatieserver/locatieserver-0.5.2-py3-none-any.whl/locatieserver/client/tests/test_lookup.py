from locatieserver.client import lookup


def test_lookup() -> None:

    result = lookup("adr-bf54db721969487ed33ba84d9973c702")

    assert result.response.num_found == 1
