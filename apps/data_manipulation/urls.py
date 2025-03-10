from django.urls import path
from . import views

urlpatterns = [
    path(
        "api/summary/<int:company_id>/",
        views.summary_by_year_and_company,
        name="summary_by_year_and_company",
    ),
    path("api/upload-excel/", views.upload_excel, name="upload_excel"),
    path("api/data/year/<int:year>/", views.data_for_year, name="data_for_year"),
    path(
        "api/data/company/<int:company_id>/mineral/<int:mineral_id>/",
        views.data_for_company_and_mineral,
        name="data_for_company_and_mineral",
    ),
    path(
        "api/data/summary/year/<int:company_id>/",
        views.summary_by_year,
        name="summary_by_year",
    ),
    path(
        "api/data/company/<int:company_id>/minerals/",
        views.data_for_company_all_minerals,
        name="data_for_company_all_minerals",
    ),
]
