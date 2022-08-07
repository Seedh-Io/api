from backend_api.helpers.enum_helper import BaseEnum


class OrderStateEnum(BaseEnum):
    CREATED = ('Created', 10)
    PROCESSING = ('Payment Processing', 20)
    COMPLETED = ('Payment Completed', 30)
    REFUNDED = ('Refunded', 40)
    FAILED = ('Payment Processed', 50)
    ISSUE = ('Issue', 60)


class OrderTypeEnum(BaseEnum):
    PACKAGE = ('Package Purchase', (1, "pck"))
    RECHARGE = ('Recharge', (2, "rcg"))

    @property
    def val(self):
        return self.data[0]

    @property
    def initial(self):
        return self.data[1]
