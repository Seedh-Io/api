from django.urls import path

from packages.views import PackageLCView, PackageRUDView

PackageAdminUrls = [
    path("", PackageLCView.as_view(), name="lc"),
    path("<id:uuid>", PackageRUDView.as_view(), name="lc")
]

PackageBusinessUrls = [

]
