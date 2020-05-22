"""
Automated Test module for Company model .
"""
import json
import pathlib

from django.test import TestCase

from company.models import Companies
from company.serializer import CompaniesSerializer


class CompanyTestCase(TestCase):
    def setUp(self):
        mode = 'testdata'
        with open(pathlib.Path.cwd() / f'{mode}//companies.json') as json_file:
            data = json.load(json_file)
            for each_company in data:
                serializer = CompaniesSerializer(data=each_company)
                if serializer.is_valid():
                    serializer.save()

    def test_data_loaded_properly(self):

        company = Companies.objects.get(company="NETBOOK")
        self.assertEqual(company.company, "NETBOOK")
