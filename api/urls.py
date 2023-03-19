from django.urls import path, include


urlpatterns = [
    path('merchant/', include('marchant.urls'), name='core'),
    path('customer/', include('customer.urls'), name='cutomer'),
    path('auth/', include('authentication.urls'), name='user-auth'),
    path('houses/', include('house.urls'), name='house'),
]