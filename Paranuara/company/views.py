"""
All the views related to company are present here.
"""
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser

from company.models import Companies
from company.serializer import CompaniesSerializer


class CompaniesViewset(viewsets.ModelViewSet):
    """
    This viewset provides all the basic functionality like get, put and
    post for the Company model.
    """
    parser_classes = (MultiPartParser, FormParser)
    queryset = Companies.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CompaniesSerializer
    pagination_class = None
