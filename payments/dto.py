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
