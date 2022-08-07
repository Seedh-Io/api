from django.urls import path
from orders.views import PackageOrderCreateView, RechargeOrderCreateView

OrderAdminUrls = [

]

OrderBusinessUrls = [
    path("package", PackageOrderCreateView.as_view(), name="package"),
    path("recharge", RechargeOrderCreateView.as_view(), name="recharge"),
]
