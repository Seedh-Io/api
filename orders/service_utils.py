class PackagesUtils:

    @staticmethod
    def get_package_by_id(package_id):
        from packages.repository import PackagesRepository
        return PackagesRepository.get_package_by_id(package_id)
