from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload-excel/', views.upload_excel, name='upload_excel'),
    path('api/data/year/<int:year>/', views.data_for_year, name='data_for_year'),
    path('api/data/company/<int:company_id>/mineral/<int:mineral_id>/', views.data_for_company_and_mineral, name='data_for_company_and_mineral'),
    path('api/data/summary/year/', views.summary_by_year, name='summary_by_year'),
]
