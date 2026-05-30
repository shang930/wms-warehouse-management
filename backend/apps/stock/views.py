"""Views for stock app."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from apps.stock.models import Stock, StockMovement
from apps.stock.serializers import MoveStockSerializer, StockMovementSerializer, StockSerializer

class StockViewSet(ReadOnlyModelViewSet):
    queryset = Stock.objects.select_related('goods','warehouse','bin').all()
    serializer_class = StockSerializer
    filterset_fields = ['warehouse_id','goods_id']
    search_fields = ['goods__code','goods__name','bin__code']
    ordering_fields = ['quantity','goods__code']
    ordering = ['goods__code']

    @action(detail=False)
    def overview(self, request):
        from django.db.models import Sum
        qs = Stock.objects.select_related('goods','warehouse').filter(quantity__gt=0)
        warehouse_id = request.query_params.get('warehouse_id')
        if warehouse_id: qs = qs.filter(warehouse_id=warehouse_id)
        rows = qs.values('goods_id','goods__code','goods__name','goods__unit__name','warehouse_id','warehouse__name').annotate(total=Sum('quantity'))
        goods_stock = {}
        for r in rows:
            gid = r['goods_id']
            if gid not in goods_stock:
                goods_stock[gid] = {'goods_id':gid,'goods_code':r['goods__code'],'goods_name':r['goods__name'],'unit_name':r['goods__unit__name'],'total':0}
            goods_stock[gid]['total'] += r['total']
        return Response({'code':200,'data':list(goods_stock.values())})

    @action(detail=False)
    def alerts(self, request):
        from django.db.models import Sum
        qs = Stock.objects.select_related('goods').filter(quantity__gt=0)
        warehouse_id = request.query_params.get('warehouse_id')
        if warehouse_id: qs = qs.filter(warehouse_id=warehouse_id)
        rows = qs.values('goods_id').annotate(total=Sum('quantity'))
        total_map = {r['goods_id']:r['total'] for r in rows}
        from apps.goods.models import Goods
        alerts = []
        for g in Goods.objects.filter(id__in=list(total_map.keys()), is_active=True):
            total = total_map.get(str(g.id), 0)
            if g.safety_stock > 0 and total < g.safety_stock:
                alerts.append({'goods_id':g.id,'goods_code':g.code,'goods_name':g.name,'current_qty':total,'safety_stock':g.safety_stock})
        return Response({'code':200,'data':alerts})

class StockMovementViewSet(ReadOnlyModelViewSet):
    queryset = StockMovement.objects.select_related('goods','warehouse','from_bin','to_bin','operator').all()
    serializer_class = StockMovementSerializer
    filterset_fields = ['warehouse_id','goods_id','movement_type']
    search_fields = ['goods__code','goods__name','ref_no']
    ordering = ['-created_at']

class MoveStockView(APIView):
    def post(self, request):
        serializer = MoveStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            with transaction.atomic():
                from_stock = Stock.objects.select_for_update().get(goods_id=data['goods_id'], bin_id=data['from_bin_id'])
                if from_stock.quantity < data['quantity']: return Response({'code':400,'message':'源库位库存不足'}, status=400)
                from_stock.quantity -= data['quantity']; from_stock.save()
                to_stock, _ = Stock.objects.select_for_update().get_or_create(goods_id=data['goods_id'], bin_id=data['to_bin_id'], defaults={'warehouse_id':from_stock.warehouse_id,'quantity':0})
                to_stock.quantity += data['quantity']; to_stock.save()
                StockMovement.objects.create(goods_id=data['goods_id'], warehouse_id=from_stock.warehouse_id, from_bin_id=data['from_bin_id'], to_bin_id=data['to_bin_id'], movement_type=3, quantity=data['quantity'], operator=request.user, remark=data.get('remark',''))
        except Stock.DoesNotExist: return Response({'code':400,'message':'源库位无该商品库存'}, status=400)
        self._broadcast(from_stock.warehouse_id)
        return Response({'code':200,'message':'移库成功'})

    def _broadcast(self, warehouse_id):
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)('stock_updates', {'type':'stock_changed','data':{'warehouse_id':str(warehouse_id)}})
        except Exception: pass
