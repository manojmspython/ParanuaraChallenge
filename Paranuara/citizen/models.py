"""
The Database schema or model for people in Paranuara and friendship between the
citizens are also designed here.
"""
from django.db import models
from django_mysql.models import ListTextField

from company.models import Companies


class Citizen(models.Model):
    """
    This model save the details of citizen in Paranuara.
    """
    index = models.PositiveIntegerField(primary_key=True, unique=True, blank=False, null=False)
    _id = models.CharField(max_length=128, unique=True, blank=False)
    guid = models.CharField(max_length=128, unique=True, blank=False)
    name = models.CharField(max_length=128, blank=True, null=True)
    age = models.PositiveIntegerField(default=0, blank=True, null=True)
    has_died = models.BooleanField(default=False)
    balance = models.DecimalField(default=0.0, decimal_places=2, max_digits=32)
    picture = models.CharField(max_length=256, blank=True, null=True)
    eye_color = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=16, blank=True, null=True)
    company_id = models.ForeignKey(Companies, blank=True, null=True, on_delete=models.DO_NOTHING)
    email = models.CharField(max_length=32, blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    registered = models.DateTimeField(blank=True, null=True)
    greeting = models.TextField(blank=True, null=True)
    friend = ListTextField(base_field=models.IntegerField(), size=100)

    # The ListTextField is used to save array directly to database
    tags = ListTextField(base_field=models.CharField(max_length=32), size=100)
    fruits = ListTextField(base_field=models.CharField(max_length=32), size=100)
    vegetables = ListTextField(base_field=models.CharField(max_length=32), size=100)
    myfriends = models.ManyToManyField('self', related_name='friends', blank=True, through='Friend')

    def __str__(self):
        return f"{self.index},{self.name}"

    @property
    def get_relations(self):
        """
        The property is defined so that friendship beteen different citizens can be traced.
        :return:
        """
        return Friend.objects.filter(people_index=self)


class Friend(models.Model):
    """
     This model save the details of frisnship between citizen in Paranuara.
    """
    people_index = models.ForeignKey('Citizen', related_name='from_person', on_delete=models.DO_NOTHING)
    friend_index = models.ForeignKey('Citizen', related_name='to_friend', on_delete=models.DO_NOTHING)
