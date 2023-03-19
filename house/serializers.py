from rest_framework.serializers import ModelSerializer
from .models import House, Category, Coupon, Payment, Booked
from customer.serializers import CustomerSerializer



class HouseSerializer(ModelSerializer):
    class Meta:
        model = House
        fields = ['id', 'address','active', 'cat_name', 'is_booked', 'merchant_name', 'price', 'no_of_rooms', 'images']
        
        depth = 2

        
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'        

