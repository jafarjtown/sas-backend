from django.urls import path, include
from .views import BookedHouse,BookedHouseCustomer,BookedHouseCustomerPayment


urlpatterns = [
    path('booked/check/', BookedHouseCustomer.as_view(),name='booked-house-check'),
    path('booked/<hid>/', BookedHouse.as_view(),name='booked-house'),
    path('booked/<hid>/payment/<ref_id>/', BookedHouseCustomerPayment.as_view(),name='booked-house-pay'),
    
    
]
