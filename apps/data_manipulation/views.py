from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum
from rest_framework import pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .dataprocess import cleanse_and_extract
from apps.companies.models import company, minerals, mineralsYear
from django.core.paginator import Paginator


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_excel(request):
    if request.method == "POST":
        file = request.FILES["file"]

        try:
            # Process the uploaded file
            df_cleaned, main_title = cleanse_and_extract(file)
        except Exception as e:
            return JsonResponse({"status": "failed", "error": str(e)}, status=400)

        companie, created = company.objects.get_or_create(name=main_title)

        for index, row in df_cleaned.iterrows():
            year = row[df_cleaned.columns[0]]

            for mineral_name in df_cleaned.columns[1:]:
                value = row[mineral_name]

                mineral, created = minerals.objects.get_or_create(name=mineral_name)

                mineralyear = mineralsYear(
                    companie=companie, mineral=mineral, year=year, value=value
                )

                mineralyear.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "failed"}, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def data_for_year(request, year):
    year_data = mineralsYear.objects.filter(year=year)
    data = list(year_data.values("companie__name", "mineral__name", "year", "value"))
    return JsonResponse(data, safe=False)


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "per_page"
    max_page_size = 100


# @permission_required('can view minerals year')
def data_for_company_and_mineral(request, company_id, mineral_id):
    company_data = mineralsYear.objects.filter(
        companie_id=company_id, mineral_id=mineral_id
    )
    structured_data = {}

    for entry in company_data:
        company_name = entry.companie.name
        year = entry.year
        mineral_name = entry.mineral.name
        value = entry.value

        if company_name not in structured_data:
            structured_data[company_name] = {}

        if year not in structured_data[company_name]:
            structured_data[company_name][year] = {}

        if mineral_name not in structured_data[company_name][year]:
            structured_data[company_name][year][mineral_name] = []

        structured_data[company_name][year][mineral_name].append(value)

        flattened_data = []
    for company, years in structured_data.items():
        for year, minerals in years.items():
            flattened_data.append(
                {"company": company, "year": year, "minerals": minerals}
            )

    # Apply pagination using DRF's PageNumberPagination
    paginator = CustomPagination()
    paginated_data = paginator.paginate_queryset(flattened_data, request)

    # Return paginated response
    return paginator.get_paginated_response(paginated_data)


def data_for_company_all_minerals(request, company_id):
    page = int(request.GET.get("page", 1))
    items_per_page = int(request.GET.get("items_per_page", 20))
    company_data = mineralsYear.objects.filter(companie_id=company_id)

    paginator = Paginator(company_data, items_per_page)
    try:
        paginated_data = paginator.page(page)
    except:
        return JsonResponse({"error": "Invalid page number"}, status=400)

    structured_data = {}
    for entry in paginated_data:
        company_name = entry.companie.name
        year = entry.year
        mineral_name = entry.mineral.name
        value = entry.value

        if company_name not in structured_data:
            structured_data[company_name] = {}

        if year not in structured_data[company_name]:
            structured_data[company_name][year] = {}

        if mineral_name not in structured_data[company_name][year]:
            structured_data[company_name][year][mineral_name] = []

        structured_data[company_name][year][mineral_name].append(value)

        response_data = {
            "data": structured_data,
            "pagination": {
                "total_items": paginator.count,
                "items_per_page": items_per_page,
                "current_page": page,
                "total_pages": paginator.num_pages,
            },
        }

    return JsonResponse(response_data, safe=False)


def summary_by_year(request, company_id):
    summary = (
        mineralsYear.objects.filter(companie_id=company_id)
        .values("year")
        .annotate(total_value=Sum("value"))
        .order_by("year")
    )
    data = [
        {"year": item["year"], "total_value": int(item["total_value"])}
        for item in summary
    ]
    return JsonResponse(data, safe=False)


def summary_by_year_and_company(request, company_id):

    total_values = (
        mineralsYear.objects.filter(companie_id=company_id)
        .values("year")
        .annotate(total_value=Sum("value"))
    )

    total_values_dict = {item["year"]: item["total_value"] for item in total_values}

    minerals = (
        mineralsYear.objects.filter(companie_id=company_id)
        .values("year", "mineral__name")
        .annotate(mineral_value=Sum("value"))
        .order_by("year", "mineral__name")
    )

    data = {}
    for item in minerals:
        year = item["year"]
        total_value = total_values_dict.get(
            year, 1
        )  # Use 1 as default to avoid division by zero
        contribution = (item["mineral_value"] / total_value) * 100
        if year not in data:
            data[year] = []
        data[year].append(
            {
                "mineral": item["mineral__name"],
                "value": item["mineral_value"],
                "contribution": round(contribution, 2),
            }
        )

    # To ensure the sum of contributions is exactly 100%, we can normalize the contributions
    for year, minerals in data.items():
        total_contribution = sum(item["contribution"] for item in minerals)
        if total_contribution != 100:
            for item in minerals:
                item["contribution"] = round(
                    item["contribution"] * 100 / total_contribution, 2
                )

    return JsonResponse(data, safe=False)
