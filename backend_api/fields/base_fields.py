import uuid

from django.db import models


class BaseFields:
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_on = models.DateTimeField(auto_now=True, null=False, blank=False)
