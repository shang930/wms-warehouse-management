from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.customer.models import Customer
from apps.customer.serializers import CustomerSerializer, CustomerSimpleSerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filterset_fields = ['is_active']
    search_fields = ['code','name','contact_person','contact_phone']
    @action(detail=False)
    def simple(self, request):
        qs = Customer.objects.filter(is_active=True)
        return Response({'code':200,'data':CustomerSimpleSerializer(qs, many=True).data})
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted','deleted_at'])
