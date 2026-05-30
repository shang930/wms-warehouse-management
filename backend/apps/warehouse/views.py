"""Views for warehouse app."""
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.warehouse.models import Bin, Warehouse, Zone
from apps.warehouse.serializers import BinSerializer, BinSimpleSerializer, WarehouseSerializer, WarehouseSimpleSerializer, ZoneSerializer

class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filterset_fields = ['is_active']
    search_fields = ['name','code']
    @action(detail=False)
    def simple(self, request):
        qs = Warehouse.objects.filter(is_active=True)
        return Response({'code':200,'data':WarehouseSimpleSerializer(qs, many=True).data})
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted','deleted_at'])

class ZoneViewSet(ModelViewSet):
    queryset = Zone.objects.select_related('warehouse').all()
    serializer_class = ZoneSerializer
    filterset_fields = ['warehouse_id']
    search_fields = ['name','code']
    ordering = ['warehouse','sort']

class BinViewSet(ModelViewSet):
    queryset = Bin.objects.select_related('warehouse','zone').all()
    serializer_class = BinSerializer
    filterset_fields = ['warehouse_id','zone_id','attribute']
    search_fields = ['code']
    @action(detail=False)
    def simple(self, request):
        warehouse_id = request.query_params.get('warehouse_id')
        qs = Bin.objects.filter(attribute='N')
        if warehouse_id: qs = qs.filter(warehouse_id=warehouse_id)
        qs = qs.only('id','code','attribute')
        return Response({'code':200,'data':BinSimpleSerializer(qs[:500], many=True).data})
    @action(detail=False, methods=['post'])
    def batch_create(self, request):
        warehouse_id = request.data.get('warehouse_id')
        zone_id = request.data.get('zone_id')
        rows = int(request.data.get('rows', 1))
        cols = int(request.data.get('cols', 1))
        levels = int(request.data.get('levels', 1))
        row_start = request.data.get('row_start', '01')
        warehouse = Warehouse.objects.get(id=warehouse_id)
        bins = []
        for r in range(rows):
            row_code = f'{int(row_start)+r:02d}'
            for c in range(1, cols+1):
                for l in range(1, levels+1):
                    code = f'{row_code}{c:02d}{l:02d}'
                    bins.append(Bin(warehouse=warehouse, zone_id=zone_id, code=code, row=row_code, col=str(c), level=str(l)))
        Bin.objects.bulk_create(bins)
        return Response({'code':200,'message':f'成功生成 {len(bins)} 个库位'})
