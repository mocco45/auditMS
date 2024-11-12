from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/mineral-years/",
        views.MineralYearListView.as_view(),
        name="mineral_year_list",
    ),
    path("api/minerals/", views.MineralsListView.as_view(), name="minerals"),
    path("api/companies/", views.CompanyListView.as_view(), name="company_list"),
    path("api/search-company/", views.list_companies, name="list_companies"),
]
