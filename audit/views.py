import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from .models import mineralsYear, company, minerals,UserActionLog
from .dataprocess import cleanse_and_extract
from .models import CustomUser,company
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .serializers import UserSerializer,MineralYearSerializer,MineralSerializer,CompanySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from rest_framework.views import APIView
from rest_framework import generics,permissions,pagination,status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .models import mineralsYear, CustomUser
from django.contrib.auth.models import Group


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)

class VerifyTokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # If the request reaches here, the token is valid
        return Response({"message": "Token is valid"}, status=200)
    
class MineralYearListView(generics.ListAPIView, PermissionRequiredMixin):
    permission_required = 'user'
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
        return Response({
            'companies': data,
            'total': self.page.paginator.count,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages
        })
    
class CompanyListView(generics.ListAPIView):
    queryset = company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CompanyPagination

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_excel(request):
    if request.method == 'POST':
        file = request.FILES['file']
        
        try:
            # Process the uploaded file
            df_cleaned, main_title = cleanse_and_extract(file)
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=400)
        
        companie, created = company.objects.get_or_create(name=main_title)
        
        for index, row in df_cleaned.iterrows():
            year = row[df_cleaned.columns[0]]
            
            for mineral_name in df_cleaned.columns[1:]:
                value = row[mineral_name]
                
                mineral, created = minerals.objects.get_or_create(name=mineral_name)
                
                mineralyear = mineralsYear(
                    companie=companie,
                    mineral=mineral,
                    year=year,
                    value=value
                )
                
                mineralyear.save()
        
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def data_for_year(request, year):
    year_data = mineralsYear.objects.filter(year=year)
    data = list(year_data.values('companie__name', 'mineral__name', 'year', 'value'))
    return JsonResponse(data, safe=False)

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100

@permission_required('can view minerals year')
def data_for_company_and_mineral(request, company_id, mineral_id):
    company_data = mineralsYear.objects.filter(companie_id=company_id, mineral_id=mineral_id)
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
            flattened_data.append({
                "company": company,
                "year": year,
                "minerals": minerals
            })

    # Apply pagination using DRF's PageNumberPagination
    paginator = CustomPagination()
    paginated_data = paginator.paginate_queryset(flattened_data, request)

    # Return paginated response
    return paginator.get_paginated_response(paginated_data)


def data_for_company_all_minerals(request, company_id):
    company_data = mineralsYear.objects.filter(companie_id=company_id)
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

    return JsonResponse(structured_data, safe=False)

def summary_by_year(request, company_id):
    summary = mineralsYear.objects.filter(companie_id=company_id).values('year').annotate(total_value=Sum('value')).order_by('year')
    data = [{"year": item['year'], "total_value": int(item['total_value'])} for item in summary]
    return JsonResponse(data, safe=False)

def list_companies(request):
    search_query = request.GET.get('search', '')
    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 10)

    companies = company.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    paginator = Paginator(companies, per_page)
    paginated_companies = paginator.get_page(page)

    data = {
        'results': [{"id": company.id, "name": company.name, "description": company.description} for company in paginated_companies],
        'page': paginated_companies.number,
        'pages': paginator.num_pages,
        'total': paginator.count,
    }
    return JsonResponse(data, safe=False)

@permission_classes([IsAuthenticated])
def user_action_logs(request):
    logs = UserActionLog.objects.filter(user=request.user)
    data = [{
        'action': log.action,
        'timestamp': log.timestamp,
        'description': log.description
    } for log in logs]
    return JsonResponse({'status': 'success', 'logs': data})


def summary_by_year_and_company(request, company_id):

    total_values = mineralsYear.objects.filter(companie_id=company_id).values('year').annotate(total_value=Sum('value'))

    total_values_dict = {item['year']: item['total_value'] for item in total_values}

    minerals = mineralsYear.objects.filter(companie_id=company_id).values('year', 'mineral__name').annotate(
        mineral_value=Sum('value')
    ).order_by('year', 'mineral__name')

    data = {}
    for item in minerals:
        year = item['year']
        total_value = total_values_dict.get(year, 1)  # Use 1 as default to avoid division by zero
        contribution = (item['mineral_value'] / total_value) * 100
        if year not in data:
            data[year] = []
        data[year].append({
            "mineral": item['mineral__name'],
            "value": item['mineral_value'],
            "contribution": round(contribution, 2)
        })

    # To ensure the sum of contributions is exactly 100%, we can normalize the contributions
    for year, minerals in data.items():
        total_contribution = sum(item['contribution'] for item in minerals)
        if total_contribution != 100:
            for item in minerals:
                item['contribution'] = round(item['contribution'] * 100 / total_contribution, 2)

    return JsonResponse(data, safe=False)

@api_view(['POST'])
def assign_role(request):
    user_id = request.data.get('user_id')
    role_id = request.data.get('role_id')
    
    try:
        user = CustomUser.objects.get(id=user_id)
        role = Group.objects.get(id=role_id)
        
        user.groups.add(role)
        return Response({"message":"Role assigned successfully"}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

    


