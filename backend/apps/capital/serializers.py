from rest_framework import serializers
from apps.capital.models import Asset, Pallet

class AssetSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True, default='')
    custodian_name = serializers.CharField(source='custodian.username', read_only=True, default='')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta: model = Asset; fields = ['id','code','name','category','status','status_display','warehouse','warehouse_name','purchase_date','purchase_price','custodian','custodian_name','remark','created_at']

class PalletSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    class Meta: model = Pallet; fields = ['id','code','warehouse','warehouse_name','max_capacity','is_active','created_at']
