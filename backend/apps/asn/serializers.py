"""Serializers for ASN app."""
from rest_framework import serializers
from apps.asn.models import ASN, ASNItem

class ASNItemSerializer(serializers.ModelSerializer):
    goods_code = serializers.CharField(source='goods.code', read_only=True)
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    unit_name = serializers.CharField(source='goods.unit.name', read_only=True)
    target_bin_code = serializers.CharField(source='target_bin.code', read_only=True, default='')
    class Meta: model = ASNItem; fields = ['id','asn','goods','goods_code','goods_name','unit_name','quantity','actual_quantity','target_bin','target_bin_code','unit_price','remark','created_at']; read_only_fields = ['asn']

class ASNItemCreateSerializer(serializers.ModelSerializer):
    class Meta: model = ASNItem; fields = ['goods','quantity','target_bin','unit_price','remark']

class ASNSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    items = ASNItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta: model = ASN; fields = ['id','asn_no','supplier','supplier_name','warehouse','warehouse_name','status','status_display','expected_time','actual_time','total_quantity','total_amount','operator','operator_name','remark','items','created_at','updated_at']; read_only_fields = ['asn_no','operator']

class ASNCreateSerializer(serializers.ModelSerializer):
    items = ASNItemCreateSerializer(many=True, write_only=True)
    class Meta: model = ASN; fields = ['supplier','warehouse','expected_time','total_amount','remark','items']
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        from datetime import datetime
        today = datetime.now().strftime('%Y%m%d')
        count = ASN.objects.filter(asn_no__startswith=f'ASN{today}').count() + 1
        validated_data['operator'] = self.context['request'].user
        validated_data['asn_no'] = f'ASN{today}{count:04d}'
        validated_data['total_quantity'] = sum(it['quantity'] for it in items_data)
        asn = ASN.objects.create(**validated_data)
        ASNItem.objects.bulk_create([ASNItem(asn=asn, **item_data) for item_data in items_data])
        return asn

class ASNStatusSerializer(serializers.Serializer):
    status = serializers.IntegerField(min_value=2, max_value=4)
    items = serializers.ListField(child=serializers.DictField(child=serializers.CharField()), required=False)
