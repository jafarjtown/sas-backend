
from rest_framework import generics

from .serializers import House, HouseSerializer


class DisplayHouses(generics.ListAPIView):
    queryset = House.objects.filter(active =True, booked=None)
    serializer_class = HouseSerializer

