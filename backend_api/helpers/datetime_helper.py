from django.utils import timezone


class DateTimeHelper:

    @staticmethod
    def get_current_datetime():
        return timezone.now()
