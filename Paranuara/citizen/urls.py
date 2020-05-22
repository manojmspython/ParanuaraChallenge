"""
Router definition for Citizen model
"""
from django.urls import path
from rest_framework import routers

from citizen.views import CitizenViewset, ParanuaraViewset

router = routers.DefaultRouter()
router.register('citizenapi', CitizenViewset, 'citizen')

urlpatterns = router.urls
urlpatterns.extend([
    path(r'getEmployees/<keyword>=<match>', ParanuaraViewset.as_view({'get': 'search_employee'}), name='citizen'),
    path(r'getFood/<keyword>=<match>', ParanuaraViewset.as_view({'get': 'get_favourites'}), name='citizen'),
    path(r'findFriends/<keyword>=<match>', ParanuaraViewset.as_view({'get': 'find_friends'}), name='citizen'),
])
