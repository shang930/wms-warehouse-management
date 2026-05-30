"""Base model mixins for all WMS models."""
import uuid
from django.db import models

class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    class Meta: abstract = True

class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name='已删除')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='删除时间')
    class Meta: abstract = True
