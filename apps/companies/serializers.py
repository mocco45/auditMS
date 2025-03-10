from rest_framework import serializers
from apps.companies.models import company, minerals, mineralsYear


class MineralYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = mineralsYear
        fields = "__all__"


class MineralSerializer(serializers.ModelSerializer):
    class Meta:
        model = minerals
        fields = "__all__"


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = company
        fields = "__all__"
