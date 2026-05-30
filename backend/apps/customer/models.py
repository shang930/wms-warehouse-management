"""Customer models."""
from django.db import models
from utils.mixins import UUIDModel, SoftDeleteModel

class Customer(UUIDModel, SoftDeleteModel):
    code = models.CharField(max_length=30, unique=True, verbose_name='客户编码')
    name = models.CharField(max_length=200, verbose_name='客户名称')
    contact_person = models.CharField(max_length=50, null=True, blank=True, verbose_name='联系人')
    contact_phone = models.CharField(max_length=30, null=True, blank=True, verbose_name='联系电话')
    email = models.EmailField(null=True, blank=True, verbose_name='邮箱')
    shipping_address = models.TextField(null=True, blank=True, verbose_name='收货地址')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta: db_table = 'customer'; verbose_name = '客户'; verbose_name_plural = verbose_name; ordering = ['code']
    def __str__(self): return f'[{self.code}] {self.name}'
