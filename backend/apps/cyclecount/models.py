"""Cycle count / inventory check models."""
from django.db import models
from utils.mixins import UUIDModel

class CycleCount(UUIDModel):
    STATUS_CHOICES = ((1,'草稿'),(2,'盘点中'),(3,'已完成'),(4,'已调整'))
    count_no = models.CharField(max_length=50, unique=True, verbose_name='盘点单号')
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT, related_name='cycle_counts', verbose_name='盘点仓库')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    planned_date = models.DateField(null=True, blank=True, verbose_name='计划盘点日期')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    operator = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='cycle_counts', verbose_name='操作人')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta: db_table = 'cycle_count'; verbose_name = '盘点单'; verbose_name_plural = verbose_name; ordering = ['-created_at']
    def __str__(self): return self.count_no

class CountRecord(UUIDModel):
    cycle_count = models.ForeignKey(CycleCount, on_delete=models.CASCADE, related_name='records', verbose_name='盘点单')
    goods = models.ForeignKey('goods.Goods', on_delete=models.PROTECT, related_name='count_records', verbose_name='商品')
    bin = models.ForeignKey('warehouse.Bin', on_delete=models.PROTECT, related_name='count_records', verbose_name='库位')
    system_quantity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='系统数量')
    actual_quantity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='实盘数量')
    difference = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='差异')
    counter = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='count_records', verbose_name='盘点人')
    class Meta: db_table = 'count_record'; verbose_name = '盘点记录'; verbose_name_plural = verbose_name; ordering = ['created_at']
    def save(self, *args, **kwargs):
        self.difference = (self.actual_quantity or 0) - (self.system_quantity or 0)
        super().save(*args, **kwargs)
    def __str__(self): return f'{self.goods.name} @ {self.bin.code} diff={self.difference}'
