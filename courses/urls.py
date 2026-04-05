from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list_view, name='course-list'),
    path('create/', views.course_create_view, name='course-create'),
    path('<int:pk>/', views.course_detail_view, name='course-detail'),
    path('<int:pk>/edit/', views.course_edit_view, name='course-edit'),
]