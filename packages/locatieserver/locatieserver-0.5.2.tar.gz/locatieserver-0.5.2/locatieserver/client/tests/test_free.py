from locatieserver.client import free


def test_free():
    result = free("Bolstraat and Utrecht and type:adres")

    assert result.response.num_found == 165

    return result
