from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import mineralsYear, minerals, company
from .serializers import MineralYearSerializer, MineralSerializer, CompanySerializer


class MineralYearListView(generics.ListAPIView, PermissionRequiredMixin):
    permission_required = "user"
    queryset = mineralsYear.objects.all()
    serializer_class = MineralYearSerializer
    permission_classes = [IsAuthenticated]


class MineralsListView(generics.ListAPIView):
    queryset = minerals.objects.all()
    serializer_class = MineralSerializer
    permission_classes = [IsAuthenticated]


class CompanyPagination(pagination.PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "companies": data,
                "total": self.page.paginator.count,
                "page": self.page.number,
                "pages": self.page.paginator.num_pages,
            }
        )


class CompanyListView(generics.ListAPIView):
    queryset = company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CompanyPagination


def list_companies(request):
    search_query = request.GET.get("search", "")
    page = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 10)

    companies = company.objects.filter(
        Q(name__icontains=search_query) | Q(description__icontains=search_query)
    )
    paginator = Paginator(companies, per_page)
    paginated_companies = paginator.get_page(page)

    data = {
        "results": [
            {"id": company.id, "name": company.name, "description": company.description}
            for company in paginated_companies
        ],
        "page": paginated_companies.number,
        "pages": paginator.num_pages,
        "total": paginator.count,
    }
    return JsonResponse(data, safe=False)
