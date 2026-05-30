"""Views for DN — outbound management."""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction, models as db_models
from django.utils import timezone
from rest_framework import serializers as drf_serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.dn.models import DN, DNItem
from apps.dn.serializers import DNCreateSerializer, DNSerializer, DNStatusSerializer
from apps.stock.models import Stock, StockMovement

class DNViewSet(ModelViewSet):
    queryset = DN.objects.select_related('customer','warehouse','operator').prefetch_related('items__goods').all()
    filterset_fields = ['status','customer_id','warehouse_id']
    search_fields = ['dn_no','customer__name','tracking_no']
    ordering = ['-created_at']

    def get_serializer_class(self): return DNCreateSerializer if self.action == 'create' else DNSerializer
    def get_queryset(self): return self.queryset if self.action in ('list','retrieve') else DN.objects.all()

    def perform_destroy(self, instance):
        if instance.status != 1: raise drf_serializers.ValidationError('只有草稿状态的出库单可以删除')
        instance.delete()

    @action(detail=True, methods=['patch'], url_path='status')
    def change_status(self, request, pk=None):
        dn = self.get_object()
        ser = DNStatusSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        new_status = ser.validated_data['status']
        self._validate_transition(dn.status, new_status)
        if new_status == 2: self._validate_stock(dn)
        elif new_status == 3: self._do_picking(dn, ser.validated_data.get('items', []))
        elif new_status == 4: self._do_ship(dn, ser.validated_data)
        dn.status = new_status
        update_fields = ['status']
        if new_status == 3: dn.actual_time = timezone.now(); update_fields.append('actual_time')
        dn.save(update_fields=update_fields)
        self._broadcast(dn.warehouse_id)
        return Response({'code':200,'message':f'状态已更新为: {dn.get_status_display()}'})

    def _validate_transition(self, current, target):
        if target != current + 1: raise drf_serializers.ValidationError(f'状态只能从 {current} 转为 {current+1}')

    def _validate_stock(self, dn):
        errors = []
        for item in dn.items.all():
            total = Stock.objects.filter(goods_id=item.goods_id, warehouse_id=dn.warehouse_id).aggregate(t=db_models.Sum('quantity'))['t'] or 0
            if total < item.quantity: errors.append(f'{item.goods.name}: 库存不足 (需要{item.quantity}, 可用{total})')
        if errors: raise drf_serializers.ValidationError({'stock': errors})

    def _do_picking(self, dn, items_data):
        item_map = {str(it['id']):it for it in items_data} if items_data else {}
        for item in dn.items.all():
            actual = item.quantity
            if str(item.id) in item_map: actual = item_map[str(item.id)].get('actual_quantity', item.quantity)
            item.actual_quantity = actual; item.save(update_fields=['actual_quantity'])

    def _do_ship(self, dn, validated_data):
        tracking_no = validated_data.get('tracking_no')
        if tracking_no: dn.tracking_no = tracking_no; dn.save(update_fields=['tracking_no'])
        for item in dn.items.all():
            actual_qty = item.actual_quantity or item.quantity
            if item.source_bin:
                try:
                    stock = Stock.objects.select_for_update().get(goods_id=item.goods_id, warehouse_id=dn.warehouse_id, bin_id=item.source_bin_id)
                    stock.quantity = max(0, stock.quantity - actual_qty); stock.save(update_fields=['quantity'])
                except Stock.DoesNotExist: pass
            else:
                stocks = Stock.objects.select_for_update().filter(goods_id=item.goods_id, warehouse_id=dn.warehouse_id, quantity__gt=0).order_by('created_at')
                remaining = actual_qty
                for st in stocks:
                    deduct = min(st.quantity, remaining)
                    st.quantity -= deduct; st.save(update_fields=['quantity'])
                    remaining -= deduct
                    if remaining <= 0: break
            StockMovement.objects.create(goods_id=item.goods_id, warehouse_id=dn.warehouse_id, from_bin_id=item.source_bin_id, movement_type=2, quantity=actual_qty, ref_no=dn.dn_no, ref_type='DN', operator=self.request.user)

    def _broadcast(self, warehouse_id):
        try:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)('stock_updates', {'type':'stock_changed','data':{'warehouse_id':str(warehouse_id)}})
        except Exception: pass
