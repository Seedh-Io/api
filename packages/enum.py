from backend_api.helpers.enum_helper import BaseEnum


class PackageStatusEnum(BaseEnum):
    ACTIVE = ("Active", 1)
    IN_ACTIVE = ("In Active", 2)
    DELETED = ("Deleted", 3)
