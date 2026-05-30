"""Serializers for cyclecount app."""
from rest_framework import serializers
from apps.cyclecount.models import CountRecord, CycleCount

class CountRecordSerializer(serializers.ModelSerializer):
    goods_code = serializers.CharField(source='goods.code', read_only=True)
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    bin_code = serializers.CharField(source='bin.code', read_only=True)
    counter_name = serializers.CharField(source='counter.username', read_only=True)
    class Meta: model = CountRecord; fields = ['id','cycle_count','goods','goods_code','goods_name','bin','bin_code','system_quantity','actual_quantity','difference','counter','counter_name']; read_only_fields = ['difference']

class CycleCountSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    operator_name = serializers.CharField(source='operator.username', read_only=True)
    records = CountRecordSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    total_items = serializers.SerializerMethodField()
    diff_items = serializers.SerializerMethodField()
    class Meta: model = CycleCount; fields = ['id','count_no','warehouse','warehouse_name','status','status_display','planned_date','completed_date','operator','operator_name','remark','records','total_items','diff_items','created_at','updated_at']
    def get_total_items(self, obj): return obj.records.count()
    def get_diff_items(self, obj): return obj.records.exclude(difference=0).count()
