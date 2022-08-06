from backend_api.helpers.enum_helper import BaseEnum


class BusinessRolesEnum(BaseEnum):
    OWNER = ("Owner", (1, "With all permissions"))
    ADMIN = ("Admin", (10, "Can make audiences and manage funds"))
    REPORTER = ("Reporter", (20, "Can download reports"))

    @property
    def val(self):
        return self.data[0]

    @property
    def description(self):
        return self.data[1]


class BusinessUserStatusEnum(BaseEnum):
    ACTIVE = ("Active", 1)
    DISABLED = ("Disabled", 2)
    BLOCKED = ("Blocked", 3)
    DELETED = ("Deleted", 4)


class BusinessStatusEnum(BaseEnum):
    ACTIVE = ("Active", 1)
    DISABLED = ("Disabled", 2)
    BLOCKED = ("Blocked", 3)
    DELETED = ("Deleted", 4)


class BusinessReferenceTypeEnum(BaseEnum):
    ORDER = ("Order", 1)
    RECHARGE = ("Recharge", 2)
