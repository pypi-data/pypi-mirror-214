from finance_enums import Country


class TestCountry:
    def test_country_basic(self):
        assert len(Country.members()) == 250
        assert str(Country.US) == "United States of America"
