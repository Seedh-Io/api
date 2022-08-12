"""backend_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from business.urls import BusinessUrls, AdminBusinessUrls
from orders.urls import OrderAdminUrls, OrderBusinessUrls
from packages.urls import PackageBusinessUrls, PackageAdminUrls
from users.urls import UserAdminUrls, UserBusinessUrls
from payments.urls import PaymentAdminUrls, PaymentBusinessUrls

register_urls = {
    "user": (UserAdminUrls, UserBusinessUrls),
    "business": (AdminBusinessUrls, BusinessUrls),
    "packages": (PackageAdminUrls, PackageBusinessUrls),
    "orders": (OrderAdminUrls, OrderBusinessUrls),
    "payment": (PaymentAdminUrls, PaymentBusinessUrls),
}


def generate_urls(url_type):
    urls = []
    for register_url in register_urls:
        index = 1 if url_type == "business" else 0
        url = "" if url_type == register_url else register_url + "/"
        url_obj = register_urls[register_url][index]
        urls.append(path(f"{url}", include((url_obj, register_url), namespace=register_url)))
    return urls


urlpatterns = [
    path("api/admin/", include((generate_urls("admin"), "backend_api"), namespace="admin")),
    path("api/business/", include((generate_urls("business"), "backend_api"), namespace="business")),
]
