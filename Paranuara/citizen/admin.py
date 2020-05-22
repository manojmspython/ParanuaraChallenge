"""
The URl's which needs to be displayed on the Django Admin pages needs to be registered here.
"""
from django.contrib import admin

from citizen.models import Citizen, Friend

admin.site.site_header = "Companies Api"

admin.site.register(Citizen)
admin.site.register(Friend)
