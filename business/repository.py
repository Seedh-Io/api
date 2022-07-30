from business.models import BusinessModel


class BusinessRepository:

    @staticmethod
    def get_active_business_for_user(user_id: str) -> [None, BusinessModel]:
        from business.models import BusinessUserModel
        return BusinessUserModel.active_objects.get_active_business_for_user(user_id)
