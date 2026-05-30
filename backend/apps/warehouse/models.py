"""Warehouse, Zone, Bin models."""
from django.db import models
from utils.mixins import UUIDModel, SoftDeleteModel

class Warehouse(UUIDModel, SoftDeleteModel):
    name = models.CharField(max_length=100, verbose_name='仓库名称')
    code = models.CharField(max_length=30, unique=True, verbose_name='仓库编码')
    address = models.TextField(null=True, blank=True, verbose_name='仓库地址')
    area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='面积(㎡)')
    manager = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_warehouses', verbose_name='负责人')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta: db_table = 'warehouse'; verbose_name = '仓库'; verbose_name_plural = verbose_name; ordering = ['code']
    def __str__(self): return f'[{self.code}] {self.name}'

class Zone(UUIDModel):
    name = models.CharField(max_length=50, verbose_name='库区名称')
    code = models.CharField(max_length=30, verbose_name='库区编码')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='zones', verbose_name='所属仓库')
    sort = models.IntegerField(default=0, verbose_name='排序')
    class Meta: db_table = 'warehouse_zone'; verbose_name = '库区'; verbose_name_plural = verbose_name; unique_together = ['warehouse','code']; ordering = ['sort']
    def __str__(self): return f'{self.warehouse.code} / {self.name}'

class Bin(UUIDModel):
    BIN_ATTR_CHOICES = (('N','正常'),('D','损坏'),('H','暂存'),('I','检验'))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='bins', verbose_name='所属仓库')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='bins', verbose_name='所属库区')
    code = models.CharField(max_length=30, verbose_name='库位编码')
    row = models.CharField(max_length=10, null=True, blank=True, verbose_name='排')
    col = models.CharField(max_length=10, null=True, blank=True, verbose_name='列')
    level = models.CharField(max_length=10, null=True, blank=True, verbose_name='层')
    attribute = models.CharField(max_length=1, choices=BIN_ATTR_CHOICES, default='N', verbose_name='库位属性')
    length = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='长(cm)')
    width = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='宽(cm)')
    height = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='高(cm)')
    max_capacity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='最大容量')
    class Meta: db_table = 'warehouse_bin'; verbose_name = '库位'; verbose_name_plural = verbose_name; unique_together = ['warehouse','code']; ordering = ['warehouse','code']
    def __str__(self): return f'[{self.warehouse.code}] {self.code}'
