"""Views for cyclecount app."""
from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.cyclecount.models import CountRecord, CycleCount
from apps.cyclecount.serializers import CycleCountSerializer
from apps.stock.models import Stock, StockMovement

class CycleCountViewSet(ModelViewSet):
    queryset = CycleCount.objects.select_related('warehouse','operator').prefetch_related('records__goods','records__bin').all()
    serializer_class = CycleCountSerializer
    filterset_fields = ['status','warehouse_id']
    search_fields = ['count_no']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        today = timezone.now().strftime('%Y%m%d')
        count = CycleCount.objects.filter(count_no__startswith=f'CC{today}').count() + 1
        serializer.save(operator=self.request.user, count_no=f'CC{today}{count:04d}')

    @action(detail=True, methods=['post'], url_path='start')
    def start_count(self, request, pk=None):
        cc = self.get_object()
        if cc.status != 1: return Response({'code':400,'message':'只有草稿状态可以开始盘点'}, status=400)
        stocks = Stock.objects.select_related('goods','bin').filter(warehouse_id=cc.warehouse_id, quantity__gt=0)
        records = []
        for st in stocks:
            records.append(CountRecord(cycle_count=cc, goods_id=st.goods_id, bin_id=st.bin_id, system_quantity=st.quantity, counter=request.user))
        CountRecord.objects.bulk_create(records)
        cc.status = 2; cc.save(update_fields=['status'])
        return Response({'code':200,'message':f'盘点已开始，共 {len(records)} 条盘点记录'})

    @action(detail=True, methods=['post'], url_path='complete')
    def complete_count(self, request, pk=None):
        cc = self.get_object()
        if cc.status != 2: return Response({'code':400,'message':'只有盘点中状态可以完成'}, status=400)
        entries = request.data.get('entries', [])
        entry_map = {e['record_id']: e['actual_quantity'] for e in entries}
        for record in cc.records.all():
            if str(record.id) in entry_map: record.actual_quantity = entry_map[str(record.id)]; record.save(update_fields=['actual_quantity','difference'])
        cc.status = 3; cc.completed_date = timezone.now(); cc.save(update_fields=['status','completed_date'])
        return Response({'code':200,'message':'盘点已完成'})

    @action(detail=True, methods=['post'], url_path='adjust')
    def adjust(self, request, pk=None):
        cc = self.get_object()
        if cc.status != 3: return Response({'code':400,'message':'只有已完成状态可以进行库存调整'}, status=400)
        with transaction.atomic():
            for record in cc.records.filter(difference__ne=0):
                try: stock = Stock.objects.select_for_update().get(goods_id=record.goods_id, bin_id=record.bin_id)
                except Stock.DoesNotExist: stock = Stock(goods_id=record.goods_id, warehouse_id=cc.warehouse_id, bin_id=record.bin_id, quantity=0)
                old_qty = stock.quantity; stock.quantity = record.actual_quantity; stock.save()
                StockMovement.objects.create(goods_id=record.goods_id, warehouse_id=cc.warehouse_id, to_bin_id=record.bin_id, movement_type=4, quantity=record.actual_quantity - old_qty, ref_no=cc.count_no, ref_type='CYCLE_COUNT', operator=request.user, remark=f'盘点调整: 系统{old_qty}→实际{record.actual_quantity}')
            cc.status = 4; cc.save(update_fields=['status'])
        return Response({'code':200,'message':'库存已调整'})
