from rest_framework.viewsets import ModelViewSet
from apps.capital.models import Asset, Pallet
from apps.capital.serializers import AssetSerializer, PalletSerializer

class AssetViewSet(ModelViewSet):
    queryset = Asset.objects.select_related('warehouse','custodian').all()
    serializer_class = AssetSerializer
    filterset_fields = ['status','category','warehouse_id']
    search_fields = ['code','name']

class PalletViewSet(ModelViewSet):
    queryset = Pallet.objects.select_related('warehouse').all()
    serializer_class = PalletSerializer
    filterset_fields = ['is_active','warehouse_id']
    search_fields = ['code']
