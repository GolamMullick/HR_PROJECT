from django.db import models


class BaseEntityBasicAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class NameAbstract(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
