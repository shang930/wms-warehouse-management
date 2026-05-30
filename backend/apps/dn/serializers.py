"""Serializers for DN app."""
from rest_framework import serializers
from apps.dn.models import DN, DNItem

class DNItemSerializer(serializers.ModelSerializer):
    goods_code = serializers.CharField(source='goods.code', read_only=True)
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    unit_name = serializers.CharField(source='goods.unit.name', read_only=True)
    source_bin_code = serializers.CharField(source='source_bin.code', read_only=True, default='')
    class Meta: model = DNItem; fields = ['id','dn','goods','goods_code','goods_name','unit_name','quantity','actual_quantity','source_bin','source_bin_code','remark','created_at']; read_only_fields = ['dn']

class DNItemCreateSerializer(serializers.ModelSerializer):
    class Meta: model = DNItem; fields = ['goods','quantity','source_bin','remark']

class DNSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    items = DNItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    class Meta: model = DN; fields = ['id','dn_no','customer','customer_name','warehouse','warehouse_name','status','status_display','expected_time','actual_time','total_quantity','shipping_address','tracking_no','operator','operator_name','remark','items','created_at','updated_at']; read_only_fields = ['dn_no','operator']

class DNCreateSerializer(serializers.ModelSerializer):
    items = DNItemCreateSerializer(many=True, write_only=True)
    class Meta: model = DN; fields = ['customer','warehouse','expected_time','shipping_address','remark','items']
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        from datetime import datetime
        today = datetime.now().strftime('%Y%m%d')
        count = DN.objects.filter(dn_no__startswith=f'DN{today}').count() + 1
        validated_data['operator'] = self.context['request'].user
        validated_data['dn_no'] = f'DN{today}{count:04d}'
        validated_data['total_quantity'] = sum(it['quantity'] for it in items_data)
        dn = DN.objects.create(**validated_data)
        DNItem.objects.bulk_create([DNItem(dn=dn, **item_data) for item_data in items_data])
        return dn

class DNStatusSerializer(serializers.Serializer):
    status = serializers.IntegerField(min_value=2, max_value=4)
    items = serializers.ListField(child=serializers.DictField(child=serializers.CharField()), required=False)
    tracking_no = serializers.CharField(required=False, allow_blank=True)
