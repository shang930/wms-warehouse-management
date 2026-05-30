"""Asset / capital models."""
from django.db import models
from utils.mixins import UUIDModel

class Asset(UUIDModel):
    STATUS_CHOICES = ((1,'使用中'),(2,'闲置'),(3,'维修中'),(4,'已报废'))
    code = models.CharField(max_length=50, unique=True, verbose_name='资产编码')
    name = models.CharField(max_length=100, verbose_name='资产名称')
    category = models.CharField(max_length=50, verbose_name='资产类别')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT, null=True, blank=True, related_name='assets', verbose_name='所在仓库')
    purchase_date = models.DateField(null=True, blank=True, verbose_name='购置日期')
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='购置价格')
    custodian = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assets', verbose_name='保管人')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta: db_table = 'asset'; verbose_name = '资产'; verbose_name_plural = verbose_name; ordering = ['code']
    def __str__(self): return f'[{self.code}] {self.name}'

class Pallet(UUIDModel):
    code = models.CharField(max_length=50, unique=True, verbose_name='托盘编号')
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT, related_name='pallets', verbose_name='所在仓库')
    max_capacity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最大承重(kg)')
    is_active = models.BooleanField(default=True, verbose_name='可用')
    class Meta: db_table = 'pallet'; verbose_name = '托盘'; verbose_name_plural = verbose_name
    def __str__(self): return self.code
