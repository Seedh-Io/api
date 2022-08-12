from backend_api.helpers.dto_helper import BaseDataObject


class PaymentProviderResponseDTO(BaseDataObject):

    def __init__(self, **kwargs):
        self.__amount_in_cents = kwargs["amount_in_cents"]
        self.__provider_order_id = kwargs["provider_order_id"]
        self.__provider_id = kwargs["provider_id"]

    @property
    def amount_in_cents(self):
        return self.__amount_in_cents

    @property
    def provider_order_id(self):
        return self.__provider_order_id

    @property
    def provider_id(self):
        return self.__provider_id


class PaymentDTO(BaseDataObject):

    def __init__(self, **kwargs):
        self.__id = kwargs["id"]
        self.__provider = kwargs["provider"]
        self.__currency = kwargs["currency"]

    @property
    def id(self):
        return self.__id

    @property
    def provider(self):
        return self.__provider

    @property
    def currency(self):
        return self.__currency


class CreatePaymentResponseDTO(BaseDataObject):

    def __init__(self, **kwargs):
        self.__payment = PaymentDTO(**kwargs["payment"])
        self.__pg_response = PaymentProviderResponseDTO(**kwargs["pg_response"])

    @property
    def payment(self):
        return self.__payment

    @property
    def pg_response(self):
        return self.__pg_response
