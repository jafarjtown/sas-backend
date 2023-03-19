
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .serializers import HouseCreateSerializer, HouseActiveSerializer, HouseBookedSerializer, ImageSerializer

from house.serializers import HouseSerializer


from house.models import Image, House, Category

class IsMerchantPermission(IsAuthenticated):

    def has_permission(self, request, view):
        """
        If the user is merchant, then grant permission. Otherwise, authorization is required.
        """
        if request.user.is_merchant:
            return True
        return super().has_permission(request, view)

class CreateDisplayHouses(APIView):

    def get(self, request):
        houses = House.objects.filter(active=True, booked=None)
        if request.user.is_authenticated and request.user.is_merchant:
            houses = request.user.houses.all()
        serializer = HouseSerializer(houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        self.permission_classes = (IsMerchantPermission,)
        if(type(request.data) == dict):
            json_data = request.data
        else:
            json_data = request.data.dict()
        category = json_data.get('category') or 'self contain'
        if hasattr(json_data, 'category'):
            delattr(json_data, 'category')
        serializer = HouseCreateSerializer(data=json_data)
        if serializer.is_valid():
            house = serializer.save()
            house.merchant = request.user
            cat, _ = Category.objects.get_or_create(name = category)
            house.category = cat
            house.save()
            return Response({"message": "House added" }, status=status.HTTP_201_CREATED)
        return Response({
                "messages": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['GET','POST'])
@permission_classes([IsMerchantPermission])
def upload_images(request, pk):
    if request.user.houses.filter(id = pk).exists() == False:
        return Response({"message": f"you don't have House with such ID : {pk}" }, status=status.HTTP_404_NOT_FOUND)
    house = request.user.houses.get(id = pk)
    if request.method == 'POST':
        json_data = request.data.getlist('images')
        for imgs in json_data:
            f = Image.objects.create(file = imgs, address=house.address)
            house.images.add(f)
            house.save()
    serializer = ImageSerializer(house.images.all(),many=True)        
    return Response(serializer.data, status=status.HTTP_200_OK)

class RetrieveUpdateHouse(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = House.objects.filter(active=True)
    serializer_class = HouseSerializer
    permission_classes = (IsMerchantPermission,)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_merchant:
            self.queryset = request.user.houses.all()
        if self.get_object().is_booked:
            self.serializer_class = HouseBookedSerializer
        return super().get(request, *args, **kwargs)
    def update(self, request, pk, **kwargs):
        self.permission_classes = (IsMerchantPermission,)
        # self.permission_classes
        try:
            if(type(request.data) == dict):
                json_data = request.data
            else:
                json_data = request.data.dict()
            House.objects.filter(id = pk).update(**json_data)
            return Response({"success": True, "message": "update is successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False, "message": "Unknown Error ocured"}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, *args, **kwargs):
        self.permission_classes = (IsMerchantPermission,)
        return super().delete(request, *args, **kwargs) 

class RetrieveAllHouseBookedNotPay(generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    
    filter_backends = [SearchFilter]
    search_fields = ['address']
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(active = False )
        # self.se
        return super().list(request, *args, **kwargs)
    