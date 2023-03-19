from django.urls import path
from .views import CreateDisplayHouses, RetrieveUpdateHouse, RetrieveAllHouseBookedNotPay, upload_images 

app_name= 'merchant'
urlpatterns = [
    path('', CreateDisplayHouses.as_view(),name='merchant'),
    path('booked/', RetrieveAllHouseBookedNotPay.as_view(), name='ret-all-merchant'),
    path('<pk>/', RetrieveUpdateHouse.as_view(), name='ret-merchant'),
    path('<pk>/images/', upload_images, name='imgs-merchant'),
]

