"""
Router definition for Company model
"""
from rest_framework import routers

from company.views import CompaniesViewset

router = routers.DefaultRouter()
router.register('companyapi', CompaniesViewset, 'company')

urlpatterns = router.urls
