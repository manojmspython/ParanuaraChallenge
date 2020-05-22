"""
Automated Test module for citizen model and expected 3 api
"""
import json
import pathlib
from collections import defaultdict
from decimal import Decimal
from os import environ

import nltk
from dateutil import parser
from rest_framework.test import APITestCase

from citizen.models import Citizen, Friend
from company.models import Companies
from company.serializer import CompaniesSerializer

try:
    from nltk.corpus import wordnet as wn
except Exception:
    nltk.download('wordnet')
    from nltk.corpus import wordnet as wn

CATEGORY = ['people.json', 'companies.json']
DJANGO_SU_NAME = environ.get('DJANGO_SU_NAME', 'admin')
DJANGO_SU_EMAIL = environ.get('DJANGO_SU_EMAIL', '')
DJANGO_SU_PASSWORD = environ.get('DJANGO_SU_PASSWORD', 'Password@12345')


class ParanuaraViewTestBase(APITestCase):
    def setUp(self):
        mode = "testdata"
        fruits = set([w for s in wn.synset('fruit.n.01').closure(lambda s: s.hyponyms()) for w in s.lemma_names()])
        vegetables = set(
            [w for s in wn.synset('vegetable.n.01').closure(lambda s: s.hyponyms()) for w in s.lemma_names()])
        with open(pathlib.Path.cwd() / f'{mode}//companies.json') as json_file:
            data = json.load(json_file)
            for each_company in data:
                serializer = CompaniesSerializer(data=each_company)
                if serializer.is_valid():
                    serializer.save()
        with open(pathlib.Path.cwd() / f'{mode}//people.json') as json_file:
            data = json.load(json_file)
            for each_person in data:
                favourite_food = each_person.pop('favouriteFood')

                registered = parser.parse(each_person.pop('registered'))
                each_person['registered'] = registered
                balance = Decimal(each_person.pop('balance').strip('$').replace(',', ''))
                each_person['balance'] = balance
                company_id = Companies.objects.filter(index=each_person.pop('company_id')).first()
                each_person['company_id'] = company_id
                each_person['eye_color'] = each_person.pop('eyeColor')

                categorised_foods = defaultdict(list)
                for food in favourite_food:
                    if food in fruits:
                        categorised_foods['fruits'].append(food)
                    elif food in vegetables:
                        categorised_foods['vegetables'].append(food)

                each_person.update(categorised_foods)
                each_person['friend'] = [each['index'] for each in each_person.pop('friends')]
                citizen_object = Citizen(**each_person)
                citizen_object.save()
        with open(pathlib.Path.cwd() / f'{mode}//people.json') as json_file:
            data = json.load(json_file)
            for each_person in data:
                for each_friend in each_person.pop('friends'):
                    people_index = Citizen.objects.filter(index=each_person['index']).first()
                    friend_index = Citizen.objects.filter(index=each_friend['index']).first()
                    if people_index and friend_index:
                        friend_object = Friend()
                        friend_object.people_index = people_index
                        friend_object.friend_index = friend_index
                        friend_object.save()

    def test_lookup_employee(self):
        response = self.client.get("/citizen/getEmployees/company=NETBOOK")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['index'], 1)

    def test_lookup_favouritefood(self):
        response = self.client.get("http://127.0.0.1:8000/citizen/getFood/name=Carmella Lambert")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['fruits'], ['orange', 'apple', 'banana', 'strawberry'])

    def test_lookup_common_friends(self):
        response = self.client.get("/citizen/findFriends/name=Decker Mckenzie,Carmella Lambert")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['name'], 'Decker Mckenzie')
