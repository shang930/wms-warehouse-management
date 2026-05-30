"""Serializers for goods app."""
from rest_framework import serializers
from apps.goods.models import Goods, GoodsBrand, GoodsCategory, GoodsUnit

class GoodsCategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    class Meta: model = GoodsCategory; fields = ['id','name','code','sort','children']
    def get_children(self, obj):
        children = obj.children.filter(is_deleted=False).order_by('sort')
        return GoodsCategoryTreeSerializer(children, many=True).data if children else []

class GoodsCategorySerializer(serializers.ModelSerializer):
    class Meta: model = GoodsCategory; fields = ['id','name','code','parent','sort','is_deleted','created_at']

class GoodsUnitSerializer(serializers.ModelSerializer):
    class Meta: model = GoodsUnit; fields = ['id','name','code']

class GoodsBrandSerializer(serializers.ModelSerializer):
    class Meta: model = GoodsBrand; fields = ['id','name']

class GoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True, default='')
    total_stock = serializers.SerializerMethodField()
    class Meta:
        model = Goods
        fields = ['id','code','name','category','category_name','unit','unit_name','brand','brand_name','spec','barcode','image','safety_stock','max_stock','purchase_price','sale_price','is_active','remark','total_stock','created_at','updated_at']
    def get_total_stock(self, obj):
        from django.db.models import Sum
        total = obj.stocks.aggregate(t=Sum('quantity'))['t']
        return total or 0
