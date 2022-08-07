class PackagesRepository:

    @staticmethod
    def get_package_by_id(package_id):
        from packages.models import PackagesModel
        return PackagesModel.objects.get(id=package_id)
