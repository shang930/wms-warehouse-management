from rest_framework import serializers
from apps.supplier.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta: model = Supplier; fields = ['id','code','name','contact_person','contact_phone','email','address','bank_name','bank_account','tax_number','is_active','remark','created_at','updated_at']

class SupplierSimpleSerializer(serializers.ModelSerializer):
    class Meta: model = Supplier; fields = ['id','code','name']
