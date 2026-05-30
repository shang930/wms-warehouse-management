"""Views for ASN — inbound management."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers as drf_serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.asn.models import ASN, ASNItem
from apps.asn.serializers import ASNCreateSerializer, ASNSerializer, ASNStatusSerializer
from apps.stock.models import Stock, StockMovement

def _validate_asn_transition(current, target):
    if target != current + 1: raise drf_serializers.ValidationError(f'状态只能从 {current} 转为 {current + 1}，不能从 {current} 转为 {target}')

def _broadcast_stock(warehouse_id):
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('stock_updates', {'type':'stock_changed','data':{'warehouse_id':str(warehouse_id)}})
    except Exception: pass

class ASNViewSet(ModelViewSet):
    queryset = ASN.objects.select_related('supplier','warehouse','operator').prefetch_related('items__goods').all()
    filterset_fields = ['status','supplier_id','warehouse_id']
    search_fields = ['asn_no','supplier__name']
    ordering = ['-created_at']

    def get_serializer_class(self): return ASNCreateSerializer if self.action == 'create' else ASNSerializer
    def get_queryset(self): return self.queryset if self.action in ('list','retrieve') else ASN.objects.all()

    def perform_destroy(self, instance):
        if instance.status != 1: raise drf_serializers.ValidationError('只有草稿状态的入库单可以删除')
        instance.delete()

    @action(detail=True, methods=['patch'], url_path='status')
    def change_status(self, request, pk=None):
        asn = self.get_object()
        ser = ASNStatusSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        new_status = ser.validated_data['status']
        _validate_asn_transition(asn.status, new_status)
        if new_status == 4: self._do_putaway(asn, ser.validated_data.get('items', []))
        asn.status = new_status
        update_fields = ['status']
        if new_status == 2: asn.actual_time = timezone.now(); update_fields.append('actual_time')
        asn.save(update_fields=update_fields)
        _broadcast_stock(asn.warehouse_id)
        return Response({'code':200,'message':f'状态已更新为: {asn.get_status_display()}'})

    def _do_putaway(self, asn, items_data):
        item_map = {str(it['id']):it for it in items_data} if items_data else {}
        for item in asn.items.all():
            actual_qty = item.quantity
            if str(item.id) in item_map: actual_qty = item_map[str(item.id)].get('actual_quantity', item.quantity)
            item.actual_quantity = actual_qty; item.save(update_fields=['actual_quantity'])
            if item.target_bin and actual_qty > 0:
                stock, _ = Stock.objects.get_or_create(goods_id=item.goods_id, warehouse_id=asn.warehouse_id, bin_id=item.target_bin_id, defaults={'quantity':0})
                stock.quantity += actual_qty; stock.save(update_fields=['quantity'])
                StockMovement.objects.create(goods_id=item.goods_id, warehouse_id=asn.warehouse_id, to_bin_id=item.target_bin_id, movement_type=1, quantity=actual_qty, ref_no=asn.asn_no, ref_type='ASN', operator=self.request.user)
