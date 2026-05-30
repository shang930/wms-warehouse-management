from django.contrib import admin
from apps.goods.models import Goods, GoodsBrand, GoodsCategory, GoodsUnit

admin.site.register(GoodsCategory)
admin.site.register(GoodsUnit)

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['code','name','category','unit','brand','is_active']
    list_filter = ['category','is_active']
    search_fields = ['code','name','barcode']

@admin.register(GoodsBrand)
class GoodsBrandAdmin(admin.ModelAdmin): pass
