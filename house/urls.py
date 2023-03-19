
from django.urls import path 
from .views import DisplayHouses

app_name = 'house'

urlpatterns = [
    path('', DisplayHouses.as_view(), name='houses')
]