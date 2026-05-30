from rest_framework import serializers
from apps.customer.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta: model = Customer; fields = ['id','code','name','contact_person','contact_phone','email','shipping_address','is_active','remark','created_at','updated_at']

class CustomerSimpleSerializer(serializers.ModelSerializer):
    class Meta: model = Customer; fields = ['id','code','name']
