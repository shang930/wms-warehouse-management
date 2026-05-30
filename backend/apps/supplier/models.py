"""Supplier models."""
from django.db import models
from utils.mixins import UUIDModel, SoftDeleteModel

class Supplier(UUIDModel, SoftDeleteModel):
    code = models.CharField(max_length=30, unique=True, verbose_name='供应商编码')
    name = models.CharField(max_length=200, verbose_name='供应商名称')
    contact_person = models.CharField(max_length=50, null=True, blank=True, verbose_name='联系人')
    contact_phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='联系电话')
    email = models.EmailField(null=True, blank=True, verbose_name='邮箱')
    address = models.TextField(null=True, blank=True, verbose_name='地址')
    bank_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='开户行')
    bank_account = models.CharField(max_length=50, null=True, blank=True, verbose_name='银行账号')
    tax_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='税号')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta: db_table = 'supplier'; verbose_name = '供应商'; verbose_name_plural = verbose_name; ordering = ['code']
    def __str__(self): return f'[{self.code}] {self.name}'
