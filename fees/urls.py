from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_fee_list_view, name='my-fees'),
    path('list/', views.fee_list_view, name='fee-list'),
    path('create/', views.fee_create_view, name='fee-create'),
    path('<int:pk>/', views.fee_detail_view, name='fee-detail'),
]