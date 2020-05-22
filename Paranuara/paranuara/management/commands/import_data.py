import json
import pathlib
from collections import defaultdict
from decimal import Decimal
from os import listdir, system, environ

import nltk
from dateutil import parser
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from jsonschema import validate

from citizen.models import Citizen, Friend
from company.models import Companies
from company.serializer import CompaniesSerializer
from json_custom_schema.custom_schema import SCHEMA

try:
    from nltk.corpus import wordnet as wn
except Exception:
    nltk.download('wordnet')
    from nltk.corpus import wordnet as wn

CATEGORY = ['people.json', 'companies.json']
DJANGO_SU_NAME = environ.get('DJANGO_SU_NAME', 'admin')
DJANGO_SU_EMAIL = environ.get('DJANGO_SU_EMAIL', '')
DJANGO_SU_PASSWORD = environ.get('DJANGO_SU_PASSWORD', 'Password@12345')


def import_data(mode):
    """
    This module can extend the cli for mange.py provided by Django
    and this utility is used to load data into database.

    :param mode:
    :return: None
    """
    print("Caching fruits and vegetables")
    # Fruits and vegetables are loaded upfront so that favourite foods can be segregated accordingly.
    fruits = set([w for s in wn.synset('fruit.n.01').closure(lambda s: s.hyponyms()) for w in s.lemma_names()])
    vegetables = set(
        [w for s in wn.synset('vegetable.n.01').closure(lambda s: s.hyponyms()) for w in s.lemma_names()])

    all_resources = listdir(pathlib.Path.cwd() / f'{mode}')
    if set(all_resources) != set(CATEGORY):
        raise CommandError(f"Please add these file in {mode} folder: {CATEGORY}")

    system('python manage.py flush --no-input')

    superuser = User.objects.create_superuser(
        username=DJANGO_SU_NAME,
        email=DJANGO_SU_EMAIL,
        password=DJANGO_SU_PASSWORD)
    superuser.save()
    print("Started loading data")
    with open(pathlib.Path.cwd() / f'{mode}//companies.json') as json_file:
        data = json.load(json_file)
        validate(instance=data, schema=SCHEMA['companies'])
        for each_company in data:
            serializer = CompaniesSerializer(data=each_company)
            if serializer.is_valid():
                serializer.save()

    with open(pathlib.Path.cwd() / f'{mode}//people.json') as json_file:
        data = json.load(json_file)
        validate(instance=data, schema=SCHEMA['people'])
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
    print("Completed Loading the Data")


class Command(BaseCommand):
    help = 'Import data from json file'

    def handle(self, *args, **options):
        try:
            import_data("resources")
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise CommandError(f"Message: {e}")
