from django.urls import path
from . import views

urlpatterns = [
    path('fee/<int:fee_id>/', views.payment_create_view, name='payment-create'),
    path('history/', views.payment_history_view, name='payment-history'),
]