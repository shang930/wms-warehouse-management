"""Serializers for stock app."""
from rest_framework import serializers
from apps.stock.models import Stock, StockMovement

class StockSerializer(serializers.ModelSerializer):
    goods_code = serializers.CharField(source='goods.code', read_only=True)
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    unit_name = serializers.CharField(source='goods.unit.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    bin_code = serializers.CharField(source='bin.code', read_only=True)
    available_quantity = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    class Meta: model = Stock; fields = ['id','goods','goods_code','goods_name','unit_name','warehouse','warehouse_name','bin','bin_code','quantity','locked_quantity','available_quantity']

class StockMovementSerializer(serializers.ModelSerializer):
    goods_code = serializers.CharField(source='goods.code', read_only=True)
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    from_bin_code = serializers.CharField(source='from_bin.code', read_only=True, default='')
    to_bin_code = serializers.CharField(source='to_bin.code', read_only=True, default='')
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    class Meta: model = StockMovement; fields = ['id','goods','goods_code','goods_name','warehouse','warehouse_name','from_bin','from_bin_code','to_bin','to_bin_code','movement_type','quantity','ref_no','ref_type','operator','operator_name','remark','created_at']

class MoveStockSerializer(serializers.Serializer):
    goods_id = serializers.UUIDField()
    from_bin_id = serializers.UUIDField()
    to_bin_id = serializers.UUIDField()
    quantity = serializers.DecimalField(max_digits=15, decimal_places=2)
    remark = serializers.CharField(required=False, allow_blank=True, default='')
