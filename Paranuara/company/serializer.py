"""
The Different Serializers for Company Model are provided here.
"""
from rest_framework import serializers

from company.models import Companies


class CompaniesSerializer(serializers.ModelSerializer):
    """
    Serializer for Company model.
    """
    class Meta:
        model = Companies
        fields = '__all__'
