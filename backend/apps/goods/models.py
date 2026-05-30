"""Goods (product) models."""
from django.db import models
from utils.mixins import UUIDModel, SoftDeleteModel

class GoodsCategory(UUIDModel, SoftDeleteModel):
    name = models.CharField(max_length=50, verbose_name='分类名称')
    code = models.CharField(max_length=30, unique=True, verbose_name='分类编码')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='上级分类')
    sort = models.IntegerField(default=0, verbose_name='排序')
    class Meta: db_table = 'goods_category'; verbose_name = '商品分类'; verbose_name_plural = verbose_name; ordering = ['sort']
    def __str__(self): return self.name

class GoodsUnit(UUIDModel):
    name = models.CharField(max_length=30, unique=True, verbose_name='单位名称')
    code = models.CharField(max_length=10, unique=True, verbose_name='单位编码')
    class Meta: db_table = 'goods_unit'; verbose_name = '商品单位'; verbose_name_plural = verbose_name
    def __str__(self): return self.name

class GoodsBrand(UUIDModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='品牌名称')
    class Meta: db_table = 'goods_brand'; verbose_name = '商品品牌'; verbose_name_plural = verbose_name
    def __str__(self): return self.name

class Goods(UUIDModel, SoftDeleteModel):
    code = models.CharField(max_length=50, unique=True, verbose_name='商品编码')
    name = models.CharField(max_length=200, verbose_name='商品名称')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='goods', verbose_name='商品分类')
    unit = models.ForeignKey(GoodsUnit, on_delete=models.PROTECT, related_name='goods', verbose_name='计量单位')
    brand = models.ForeignKey(GoodsBrand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='品牌')
    spec = models.CharField(max_length=200, null=True, blank=True, verbose_name='规格型号')
    barcode = models.CharField(max_length=100, null=True, blank=True, verbose_name='条码')
    image = models.URLField(max_length=500, null=True, blank=True, verbose_name='商品图片')
    safety_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='安全库存')
    max_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='最大库存')
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='参考进价')
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='参考售价')
    is_active = models.BooleanField(default=True, verbose_name='启用')
    remark = models.TextField(null=True, blank=True, verbose_name='备注')
    class Meta: db_table = 'goods'; verbose_name = '商品'; verbose_name_plural = verbose_name; ordering = ['code']
    def __str__(self): return f'[{self.code}] {self.name}'
