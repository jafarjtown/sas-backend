from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

from house.models import Booked, Payment, Coupon, House

from .serializers import BookedCustomerSerializer, BookedSerializer, PaymentSerializer

class IsCustomerPermission(IsAuthenticated):

    def has_permission(self, request, view):
        """
        If the user is customer, then grant permission. Otherwise, authorization is required.
        """
        if request.user.is_merchant:
            return False
        return super().has_permission(request, view)    

class BookedHouse(generics.CreateAPIView):
    queryset = Booked.objects.all()
    serializer_class = BookedSerializer
    
    permission_classes = (IsCustomerPermission,)
    
    def create(self, request, hid, **kwargs):
        customer = request.user
        house = House.objects.get(id = hid)
        coupon = request.query_params.get('coupon') or None
        if coupon:
            price = house.price
            coupon = Coupon.objects.get(code = coupon)
            if house.coupon == coupon.name:
                price = price / 100 * coupon.percentage
        booked = Booked.objects.create(
            customer = customer,
            house = house,
            coupon = coupon
        )
        booked.at_price = price
        booked.save()
        serializer = BookedSerializer(booked)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class BookedHouseCustomer(APIView):
    queryset = Booked.objects.all()
    serializer_class = BookedSerializer
    
    permission_classes = (IsCustomerPermission,)
    
    def get(self, request, *args, **kwargs):
        customer = request.user
        if self.queryset.filter(customer=customer).exists():
            booked = self.queryset.get(customer=customer)
            serializer = BookedCustomerSerializer(booked)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'No booked to be show'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        customer = request.user
        
        if self.queryset.filter(customer=customer).exists():
            booked = self.queryset.get(customer=customer)
            booked.delete()
        # serializer = BookedCustomerSerializer(booked)
            return Response({}, status=status.HTTP_200_OK)
        return Response({'message': 'No booked to be deleted'}, status=status.HTTP_404_NOT_FOUND)
    

class BookedHouseCustomerPayment(APIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    permission_classes = (IsCustomerPermission,)
    
    def get(self, request,*args, **kwargs):
        customer = request.user
        
        booked = customer.booked
        serializer = PaymentSerializer(booked.payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request,ref_id, *args, **kwargs):
        customer = request.user
        
        booked = customer.booked
        payment = Payment.objects.create(
            user_id=customer.id,
            ref_id=ref_id
        )
        booked.payment = payment
        booked.save()
        serializer = BookedCustomerSerializer(booked)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
