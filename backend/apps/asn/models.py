"""ASN (Advance Shipping Notice) — inbound management."""
from django.db import models
from utils.mixins import UUIDModel

class ASN(UUIDModel):
    STATUS_CHOICES = ((1,'草稿'),(2,'已到货'),(3,'已卸货'),(4,'已上架'))
    asn_no = models.CharField(max_length=50, unique=True, verbose_name='入库单号')
    supplier = models.ForeignKey('supplier.Supplier', on_delete=models.PROTECT, related_name='asns', verbose_name='供应商')
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT, related_name='asns', verbose_name='目标仓库')
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    expected_time = models.DateTimeField(null=True, blank=True, verbose_name='预计到达时间')
    actual_time = models.DateTimeField(null=True, blank=True, verbose_name='实际入库时间')
    total_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='总数量')
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='总金额')
    operator = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='created_asns', verbose_name='操作人')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta:
        db_table = 'asn'; verbose_name = '入库单'; verbose_name_plural = verbose_name; ordering = ['-created_at']
        indexes = [models.Index(fields=['asn_no']), models.Index(fields=['status']), models.Index(fields=['supplier','-created_at'])]
    def __str__(self): return f'{self.asn_no} [{self.get_status_display()}]'

class ASNItem(UUIDModel):
    asn = models.ForeignKey(ASN, on_delete=models.CASCADE, related_name='items', verbose_name='入库单')
    goods = models.ForeignKey('goods.Goods', on_delete=models.PROTECT, related_name='asn_items', verbose_name='商品')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='数量')
    actual_quantity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='实收数量')
    target_bin = models.ForeignKey('warehouse.Bin', on_delete=models.PROTECT, null=True, blank=True, related_name='asn_items', verbose_name='目标库位')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='单价')
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name='备注')
    class Meta: db_table = 'asn_item'; verbose_name = '入库明细'; verbose_name_plural = verbose_name; ordering = ['created_at']
    def __str__(self): return f'{self.asn.asn_no} / {self.goods.name}'
