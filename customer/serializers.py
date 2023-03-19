from rest_framework.serializers import ModelSerializer
from authentication.models import User
# from marchant.functions import attempt_json_deserialize
from house.models import Booked, Payment

class CustomerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [ 'id', 'username']
        
class BookedSerializer(ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Booked
        fields = ['payment', 'coupon', 'customer', 'created_at', 'at_price']

class BookedCustomerSerializer(ModelSerializer):
    class Meta:
        model = Booked
        fields = ['payment', 'coupon', 'house','created_at', 'at_price']

class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'        

