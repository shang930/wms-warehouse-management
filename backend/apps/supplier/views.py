from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.supplier.models import Supplier
from apps.supplier.serializers import SupplierSerializer, SupplierSimpleSerializer

class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filterset_fields = ['is_active']
    search_fields = ['code','name','contact_person','contact_phone']
    @action(detail=False)
    def simple(self, request):
        qs = Supplier.objects.filter(is_active=True)
        return Response({'code':200,'data':SupplierSimpleSerializer(qs, many=True).data})
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted','deleted_at'])
