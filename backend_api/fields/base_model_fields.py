import uuid

from django.db import models
from django.utils import timezone


class BaseModelManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        queryset = super(BaseModelManager, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_deleted=False)
        return queryset


class BaseModelFields(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    is_deleted = models.BooleanField(null=False, blank=False, default=False)
    created_on = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_on = models.DateTimeField(auto_now=True, null=False, blank=False)
    deleted_on = models.DateTimeField(null=True, blank=False)

    objects = BaseModelManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_on = timezone.now()
        self.save()
