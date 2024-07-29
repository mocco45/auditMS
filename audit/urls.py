from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/upload-excel/', views.upload_excel, name='upload_excel'),
    path('api/data/year/<int:year>/', views.data_for_year, name='data_for_year'),
    path('api/data/company/<int:company_id>/mineral/<int:mineral_id>/', views.data_for_company_and_mineral, name='data_for_company_and_mineral'),
    path('api/data/summary/year/', views.summary_by_year, name='summary_by_year'),
    path('api/roles/', views.RoleListCreateView.as_view(), name='role_list_create'),
    path('api/roles/<int:pk>/', views.RoleDetailView.as_view(), name='role_detail'),
    path('api/permissions/', views.PermissionListView.as_view(), name='permission_list'),
    path('api/permissions/create/', views.PermissionCreateView.as_view(), name='permission_create'),
    path('api/create-user/', views.UserCreateView.as_view(), name='create_user'),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/mineral-years/', views.MineralYearListView.as_view(), name='mineral_year_list'),
    path('api/minerals/', views.MineralsListView.as_view(), name='minerals'),
    path('api/data/company/<int:company_id>/minerals/', views.data_for_company_all_minerals, name='data_for_company_all_minerals'),
    path('api/companies/', views.CompanyListView.as_view(), name='company_list'),
    path('api/search-company/', views.list_companies, name='list_companies'),
    path('api/user-action-logs/', views.user_action_logs, name='user_action_logs'),
]
