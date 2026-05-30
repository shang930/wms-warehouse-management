"""Stock and StockMovement models."""
from django.db import models
from utils.mixins import UUIDModel

class Stock(models.Model):
    goods = models.ForeignKey('goods.Goods', on_delete=models.PROTECT, related_name='stocks', verbose_name='商品')
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT, related_name='stocks', verbose_name='仓库')
    bin = models.ForeignKey('warehouse.Bin', on_delete=models.PROTECT, related_name='stocks', verbose_name='库位')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='当前数量')
    locked_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='锁定数量')
    class Meta:
        db_table = 'stock'; verbose_name = '库存'; verbose_name_plural = verbose_name
        unique_together = ['goods','warehouse','bin']
        indexes = [models.Index(fields=['goods','warehouse']), models.Index(fields=['warehouse','bin'])]
    @property
    def available_quantity(self): return self.quantity - self.locked_quantity
    def __str__(self): return f'{self.goods.name} @ {self.bin.code}: {self.quantity}'

class StockMovement(UUIDModel):
    MOVEMENT_TYPE_CHOICES = ((1,'入库'),(2,'出库'),(3,'移库'),(4,'盘点调整'),(5,'报损'))
    goods = models.ForeignKey('goods.Goods', on_delete=models.PROTECT, related_name='movements', verbose_name='商品')
    warehouse = models.ForeignKey('warehouse.Warehouse', on_delete=models.PROTECT, related_name='movements', verbose_name='仓库')
    from_bin = models.ForeignKey('warehouse.Bin', on_delete=models.PROTECT, null=True, blank=True, related_name='movements_out', verbose_name='源库位')
    to_bin = models.ForeignKey('warehouse.Bin', on_delete=models.PROTECT, null=True, blank=True, related_name='movements_in', verbose_name='目标库位')
    movement_type = models.IntegerField(choices=MOVEMENT_TYPE_CHOICES, verbose_name='变动类型')
    quantity = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='变动数量')
    ref_no = models.CharField(max_length=100, null=True, blank=True, verbose_name='关联单号')
    ref_type = models.CharField(max_length=30, null=True, blank=True, verbose_name='关联单据类型')
    operator = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='stock_movements', verbose_name='操作人')
    remark = models.CharField(max_length=300, null=True, blank=True, verbose_name='备注')
    class Meta:
        db_table = 'stock_movement'; verbose_name = '库存流水'; verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [models.Index(fields=['goods','-created_at']), models.Index(fields=['warehouse','-created_at']), models.Index(fields=['ref_no'])]
    def __str__(self): return f'[{self.get_movement_type_display()}] {self.goods.name} x{self.quantity}'
