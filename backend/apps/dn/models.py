"""DN (Delivery Note) — outbound management."""
from django.db import models
from utils.mixins import UUIDModel

class DN(UUIDModel):
    STATUS_CHOICES = ((1,'草稿'),(2,'已确认'),(3,'已拣货'),(4,'已发货'))
    dn_no = models.CharField(max_length=50, unique=True, verbose_name='出库单号')
    customer = models.ForeignKey('customer.Customer', on_delete=models.PROTECT, related_name='dns', verbose_name='客户')
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT, related_name='dns', verbose_name='出库仓库')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    expected_time = models.DateTimeField(null=True, blank=True, verbose_name='预计发货时间')
    actual_time = models.DateTimeField(null=True, blank=True, verbose_name='实际发货时间')
    total_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='总数量')
    shipping_address = models.TextField(null=True, blank=True, verbose_name='收货地址')
    tracking_no = models.CharField(max_length=100, null=True, blank=True, verbose_name='物流单号')
    operator = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='created_dns', verbose_name='操作人')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta:
        db_table = 'dn'; verbose_name = '出库单'; verbose_name_plural = verbose_name; ordering = ['-created_at']
        indexes = [models.Index(fields=['dn_no']), models.Index(fields=['status']), models.Index(fields=['customer','-created_at'])]
    def __str__(self): return f'{self.dn_no} [{self.get_status_display()}]'

class DNItem(UUIDModel):
    dn = models.ForeignKey(DN, on_delete=models.CASCADE, related_name='items', verbose_name='出库单')
    goods = models.ForeignKey('goods.Goods', on_delete=models.PROTECT, related_name='dn_items', verbose_name='商品')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='数量')
    actual_quantity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='实发数量')
    source_bin = models.ForeignKey('warehouse.Bin', on_delete=models.PROTECT, null=True, blank=True, related_name='dn_items', verbose_name='拣货库位')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='备注')
    class Meta: db_table = 'dn_item'; verbose_name = '出库明细'; verbose_name_plural = verbose_name; ordering = ['created_at']
    def __str__(self): return f'{self.dn.dn_no} / {self.goods.name}'

class PickingList(UUIDModel):
    STATUS_CHOICES = ((1,'待拣货'),(2,'拣货中'),(3,'已完成'))
    dn = models.ForeignKey(DN, on_delete=models.CASCADE, related_name='picking_lists', verbose_name='出库单')
    picker = models.ForeignKey('users.User', on_delete=models.PROTECT, null=True, blank=True, related_name='picking_lists', verbose_name='拣货人')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    completed_time = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')
    class Meta: db_table = 'picking_list'; verbose_name = '拣货单'; verbose_name_plural = verbose_name; ordering = ['-created_at']
    def __str__(self): return f'拣货单 #{self.id} [{self.get_status_display()}]'
