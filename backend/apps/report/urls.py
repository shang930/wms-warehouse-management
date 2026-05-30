"""Report URLs."""
from django.urls import path
from apps.report.views import DashboardStatsView, InboundReportView, InventoryReportView, OutboundReportView, SummaryReportView

app_name = 'reports'
urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('inbound/', InboundReportView.as_view(), name='inbound_report'),
    path('outbound/', OutboundReportView.as_view(), name='outbound_report'),
    path('inventory/', InventoryReportView.as_view(), name='inventory_report'),
    path('summary/', SummaryReportView.as_view(), name='summary_report'),
]
