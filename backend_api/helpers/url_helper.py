from backend_api import settings


class UrlHelper:

    @staticmethod
    def get_website_url(path):
        return UrlHelper.url_join(UrlHelper.get_website_host_url() + path)

    @staticmethod
    def get_website_host_url():
        match settings.ENV:
            case "development":
                protocol = "http"
            case "staging" | "production":
                protocol = "https"
            case _:
                protocol = "http"
        return protocol + "://" + settings.WEBSITE_HOST

    @staticmethod
    def url_join(*parts):
        return '/'.join([p.strip().strip('/') if p else "" for p in parts])
