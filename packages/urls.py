from django.urls import path

from packages.views import PackageLCView, PackageRUDView

PackageAdminUrls = [
    path("", PackageLCView.as_view(), name="lc"),
    path("<uuid:id>", PackageRUDView.as_view(), name="rud"),
]

PackageBusinessUrls = [

]
