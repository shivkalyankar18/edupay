from django.urls import path
from . import views

urlpatterns = [
    path('payment-collection/', views.payment_collection_report_view, name='report-payment'),
    path('fee-status/', views.fee_status_report_view, name='report-fee-status'),
    path('overdue/', views.overdue_report_view, name='report-overdue'),
]