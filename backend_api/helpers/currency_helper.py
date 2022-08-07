class CurrencyHelper:

    @staticmethod
    def get_amount_to_cents(amount) -> int:
        return int(amount * 100)

    @staticmethod
    def get_cents_to_amount(amount) -> int:
        return int(amount/100)
