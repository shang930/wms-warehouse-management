"""Report views — aggregated statistics and dashboard data."""
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.asn.models import ASN
from apps.dn.models import DN
from apps.goods.models import Goods
from apps.stock.models import Stock, StockMovement
from apps.stock.serializers import StockSerializer

class DashboardStatsView(APIView):
    def get(self, request):
        today = timezone.now().date()
        total_goods = Goods.objects.filter(is_active=True).count()
        total_stock = Stock.objects.aggregate(t=Sum('quantity'))['t'] or 0
        today_in = ASN.objects.filter(created_at__date=today, status__gte=2).count()
        today_out = DN.objects.filter(created_at__date=today, status__gte=2).count()
        pending_in = ASN.objects.filter(status__in=[1,2,3]).count()
        pending_out = DN.objects.filter(status__in=[1,2,3]).count()
        alerts = []
        for g in Goods.objects.filter(is_active=True, safety_stock__gt=0):
            total = Stock.objects.filter(goods=g).aggregate(t=Sum('quantity'))['t'] or 0
            if total < g.safety_stock:
                alerts.append({'goods_id':str(g.id),'goods_code':g.code,'goods_name':g.name,'current_qty':float(total),'safety_stock':float(g.safety_stock)})
        from datetime import timedelta
        thirty_days = today - timedelta(days=30)
        in_by_day = (ASN.objects.filter(created_at__date__gte=thirty_days, status__gte=2).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).order_by('day'))
        out_by_day = (DN.objects.filter(created_at__date__gte=thirty_days, status__gte=2).annotate(day=TruncDate('created_at')).values('day').annotate(count=Count('id')).order_by('day'))
        return Response({'code':200,'data':{'total_goods':total_goods,'total_stock':float(total_stock),'today_inbound':today_in,'today_outbound':today_out,'pending_inbound':pending_in,'pending_outbound':pending_out,'alerts':alerts,'trend':{'inbound':list(in_by_day),'outbound':list(out_by_day)}}})

class InboundReportView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date'); end_date = request.query_params.get('end_date'); supplier_id = request.query_params.get('supplier_id')
        qs = ASN.objects.filter(status=4)
        if start_date: qs = qs.filter(actual_time__date__gte=start_date)
        if end_date: qs = qs.filter(actual_time__date__lte=end_date)
        if supplier_id: qs = qs.filter(supplier_id=supplier_id)
        total = qs.count(); total_qty = qs.aggregate(t=Sum('total_quantity'))['t'] or 0
        by_supplier = qs.values('supplier__name').annotate(count=Count('id'), total_qty=Sum('total_quantity')).order_by('-count')
        return Response({'code':200,'data':{'total_orders':total,'total_quantity':float(total_qty),'by_supplier':list(by_supplier)}})

class OutboundReportView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date'); end_date = request.query_params.get('end_date'); customer_id = request.query_params.get('customer_id')
        qs = DN.objects.filter(status=4)
        if start_date: qs = qs.filter(actual_time__date__gte=start_date)
        if end_date: qs = qs.filter(actual_time__date__lte=end_date)
        if customer_id: qs = qs.filter(customer_id=customer_id)
        total = qs.count(); total_qty = qs.aggregate(t=Sum('total_quantity'))['t'] or 0
        by_customer = qs.values('customer__name').annotate(count=Count('id'), total_qty=Sum('total_quantity')).order_by('-count')
        return Response({'code':200,'data':{'total_orders':total,'total_quantity':float(total_qty),'by_customer':list(by_customer)}})

class InventoryReportView(APIView):
    def get(self, request):
        category_id = request.query_params.get('category_id'); warehouse_id = request.query_params.get('warehouse_id')
        qs = Stock.objects.filter(quantity__gt=0)
        if warehouse_id: qs = qs.filter(warehouse_id=warehouse_id)
        if category_id: qs = qs.filter(goods__category_id=category_id)
        total_qty = qs.aggregate(t=Sum('quantity'))['t'] or 0
        total_items = qs.values('goods_id').distinct().count()
        return Response({'code':200,'data':{'total_items':total_items,'total_quantity':float(total_qty),'details':StockSerializer(qs.select_related('goods','bin'), many=True).data}})

class SummaryReportView(APIView):
    def get(self, request):
        start_date = request.query_params.get('start_date'); end_date = request.query_params.get('end_date')
        in_qs = StockMovement.objects.filter(movement_type=1); out_qs = StockMovement.objects.filter(movement_type=2)
        if start_date: in_qs = in_qs.filter(created_at__date__gte=start_date); out_qs = out_qs.filter(created_at__date__gte=start_date)
        if end_date: in_qs = in_qs.filter(created_at__date__lte=end_date); out_qs = out_qs.filter(created_at__date__lte=end_date)
        in_total = in_qs.aggregate(t=Sum('quantity'))['t'] or 0
        out_total = out_qs.aggregate(t=Sum('quantity'))['t'] or 0
        current_total = Stock.objects.aggregate(t=Sum('quantity'))['t'] or 0
        return Response({'code':200,'data':{'inbound_total':float(in_total),'outbound_total':float(out_total),'current_stock':float(current_total)}})
