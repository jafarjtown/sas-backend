
from rest_framework.serializers import ModelSerializer
from house.models import House, Image

from customer.serializers import BookedSerializer

class HouseBookedSerializer(ModelSerializer):
    booked = BookedSerializer()
    class Meta:
        model = House
        fields = ['id', 'booked', 'cat_name', 'merchant_name', 'price', 'no_of_rooms', 'images']
        
        depth = 2



class HouseActiveSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = ['active']


class HouseCreateSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = ['address', 'price']

class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
