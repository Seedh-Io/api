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
from packages.urls import PackageBusinessUrls, PackageAdminUrls
from users.urls import adminUrls as UserAdminUrls, businessUrls as UserBusinessUrls

adminUrls = [
    path("user/", include((UserAdminUrls, "users"), namespace="user")),
    path("business/", include((BusinessUrls, "business"), namespace="business")),
    path("packages/", include((PackageAdminUrls, "packages"), namespace="packages"))
]

businessUrls = [
    path("user/", include((UserBusinessUrls, "users"), namespace="user")),
    path("business/", include((AdminBusinessUrls, "business"), namespace="business")),
    path("packages/", include((PackageBusinessUrls, "packages"), namespace="packages"))
]

urlpatterns = [
    path("api/admin/", include((adminUrls, "backend_api"), namespace="admin")),
    path("api/business/", include((businessUrls, "backend_api"), namespace="business")),
]
