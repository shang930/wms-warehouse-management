"""Serializers for warehouse app."""
from rest_framework import serializers
from apps.warehouse.models import Bin, Warehouse, Zone

class WarehouseSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.username', read_only=True, default='')
    zone_count = serializers.IntegerField(source='zones.count', read_only=True, default=0)
    bin_count = serializers.IntegerField(source='bins.count', read_only=True, default=0)
    class Meta: model = Warehouse; fields = ['id','name','code','address','area','manager','manager_name','is_active','remark','zone_count','bin_count','created_at','updated_at']

class WarehouseSimpleSerializer(serializers.ModelSerializer):
    class Meta: model = Warehouse; fields = ['id','name','code']

class ZoneSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    class Meta: model = Zone; fields = ['id','name','code','warehouse','warehouse_name','sort']

class BinSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    zone_name = serializers.CharField(source='zone.name', read_only=True, default='')
    current_load = serializers.SerializerMethodField()
    class Meta: model = Bin; fields = ['id','warehouse','warehouse_name','zone','zone_name','code','row','col','level','attribute','length','width','height','max_capacity','current_load','created_at']
    def get_current_load(self, obj):
        from django.db.models import Sum
        total = obj.stocks.aggregate(t=Sum('quantity'))['t']
        return total or 0

class BinSimpleSerializer(serializers.ModelSerializer):
    class Meta: model = Bin; fields = ['id','code','attribute']
