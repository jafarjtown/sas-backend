
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from rest_registration.api.views import (change_password, profile, register,
                                         register_email, reset_password,
                                         send_reset_password_link,
                                         verify_email, verify_registration)

from . import views

app_name = 'authentication'
urlpatterns = [
    path('profile/', profile, name='user'),
    path('users/', views.UserAllAPIView.as_view(), name='users'),
    path('token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('activate/<pk>/<token>', views.activate, name='activate'),
    path('send-reset-password-link/', send_reset_password_link,
         name='send-reset-password-link'),
    path('reset-password/', reset_password, name='reset-password'),
    path('register/', register, name='register'),
    path('verify-user/', verify_registration, name='verify_registration'),
    path('register-new-email/', register_email, name='register_email'),
    path('verify-email/', verify_email, name='verify_email'),
    path('change-password/', change_password, name='change_password'),
]
