import logging

from rest_framework.exceptions import NotFound

from business.models import BusinessModel


class BusinessRepository:

    @staticmethod
    def get_active_business_for_user(user_id: str) -> [None, BusinessModel]:
        from business.models import BusinessUserModel
        return BusinessUserModel.active_objects.get_active_business_for_user(user_id)

    @staticmethod
    def get_business_by_id(business_id: str) -> BusinessModel:
        try:
            return BusinessModel.objects.get(id=business_id)
        except Exception as e:
            logging.info("business_not_found", extra={"error": str(e), "business_id": business_id})
            raise NotFound("Business not found")
