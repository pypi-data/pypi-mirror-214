from finance_enums import Currency


class TestCurrency:
    def test_currency_basic(self):
        assert len(Currency.members()) == 183
        assert str(Currency.USD) == "USD"
        assert Currency.USD.name == "United States dollar"
    
    def test_noniso_currency_pennies(self):
        assert Currency("EUr") == Currency.EUX
        assert Currency("GBp") == Currency.GBX
        assert Currency("USd") == Currency.USX
