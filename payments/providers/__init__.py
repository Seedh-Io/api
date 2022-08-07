from abc import ABC, abstractmethod


class BaseProvider(ABC):

    def __init__(self, amount: int, order_id: str, currency: str):
        from payments.enum import SupportedPaymentCurrenciesEnum
        self.__amount = amount
        self.__order_id = order_id
        self.__currency = SupportedPaymentCurrenciesEnum.search_by_value(currency)
        self.__order_obj = None

    @abstractmethod
    def create_payment_order(self): pass

    @staticmethod
    @abstractmethod
    def verify_payment(order_id: str, payment_id: str, signature: str): pass

    @property
    def order_id(self):
        return self.__order_id

    @property
    def amount(self):
        return self.__amount

    @property
    def currency(self):
        return self.__currency

    @property
    def order_obj(self):
        return self.__order_obj
