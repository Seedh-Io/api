from django.utils import timezone

from datetime import timedelta


class DateTimeHelper:

    @staticmethod
    def get_current_datetime():
        return timezone.now()

    @staticmethod
    def add_seconds_to_date(seconds, date=timezone.now()):
        return date + timedelta(seconds=seconds)
