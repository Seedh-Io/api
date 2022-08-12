from backend_api.helpers.currency_helper import CurrencyHelper


class OrdersHelper:

    @staticmethod
    def get_recharge_credits(recharge_amount, business_id, check_package=False) -> int:
        from orders.service_utils import BusinessUtils
        package = None
        if check_package:
            business = BusinessUtils().get_business_by_id(business_id)
            package = business.active_package
        amount = package.get_credits_when_recharge(recharge_amount) if package else recharge_amount
        return CurrencyHelper.get_cents_to_amount(round(amount))
