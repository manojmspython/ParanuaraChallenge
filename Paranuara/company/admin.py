"""
The URl's which needs to be displayed on the Django Admin pages needs to be registered here.
"""
from django.contrib import admin
from company.models import Companies

admin.site.site_header = "Companies Api"

admin.site.register(Companies)
