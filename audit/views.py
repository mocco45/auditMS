import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from .models import mineralsYear, company, minerals,Role
from .dataprocess import cleanse_and_extract
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import CustomUser
from django.contrib.auth.models import Permission
from .serializers import PermissionSerializer,UserSerializer,RoleSerializer,MineralYearSerializer,MineralSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics,permissions

class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermissionListView(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class PermissionCreateView(generics.CreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    
class MineralYearListView(generics.ListAPIView):
    queryset = mineralsYear.objects.all()
    serializer_class = MineralYearSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

class MineralsListView(generics.ListAPIView):
    queryset = minerals.objects.all()
    serializer_class = MineralSerializer
    permission_classes = [IsAuthenticated]

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


def data_for_company_and_mineral(request, company_id, mineral_id):
    company_data = mineralsYear.objects.filter(companie_id=company_id, mineral_id=mineral_id)
    data = list(company_data.values('companie__name', 'mineral__name', 'year', 'value'))
    return JsonResponse(data, safe=False)

def summary_by_year(request):
    summary = mineralsYear.objects.values('year').annotate(total_value=Sum('value')).order_by('year')
    data = list(summary)
    return JsonResponse(data, safe=False)


