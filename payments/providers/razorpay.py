from payments.providers import BaseProvider


class RazorpayProvider(BaseProvider):
    def create_payment_order(self): pass


    @staticmethod
    def verify_payment(order_id: str, payment_id: str, signature: str):
        pass

