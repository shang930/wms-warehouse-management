"""Views for goods app."""
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.goods.models import Goods, GoodsBrand, GoodsCategory, GoodsUnit
from apps.goods.serializers import GoodsBrandSerializer, GoodsCategorySerializer, GoodsCategoryTreeSerializer, GoodsSerializer, GoodsUnitSerializer

class GoodsCategoryViewSet(ModelViewSet):
    queryset = GoodsCategory.objects.filter(is_deleted=False)
    serializer_class = GoodsCategorySerializer
    filterset_fields = ['is_active']
    search_fields = ['name','code']
    ordering = ['sort']
    @action(detail=False)
    def tree(self, request):
        roots = GoodsCategory.objects.filter(parent__isnull=True, is_deleted=False).order_by('sort')
        return Response({'code':200,'data':GoodsCategoryTreeSerializer(roots, many=True).data})
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted','deleted_at'])

class GoodsUnitViewSet(ModelViewSet):
    queryset = GoodsUnit.objects.all()
    serializer_class = GoodsUnitSerializer
    search_fields = ['name','code']

class GoodsBrandViewSet(ModelViewSet):
    queryset = GoodsBrand.objects.all()
    serializer_class = GoodsBrandSerializer
    search_fields = ['name']

class GoodsViewSet(ModelViewSet):
    queryset = Goods.objects.select_related('category','unit','brand').all()
    serializer_class = GoodsSerializer
    filterset_fields = ['category_id','is_active']
    search_fields = ['code','name','barcode','spec']
    ordering_fields = ['code','name','created_at']
    ordering = ['code']
    @action(detail=False)
    def simple(self, request):
        qs = Goods.objects.filter(is_active=True).only('id','code','name','unit_id')
        data = [{'id':g.id,'code':g.code,'name':g.name} for g in qs[:500]]
        return Response({'code':200,'data':data})
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted','deleted_at'])
