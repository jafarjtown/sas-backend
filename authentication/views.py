
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserCreateSerializer, UserSerializer
from .models import User
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
import json
from django.contrib.auth.hashers import make_password
from rest_framework import status, generics
from rest_framework.decorators import api_view,permission_classes


from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout as user_logout, login as user_login
from django.contrib.messages import add_message ,constants
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .email_token import account_activation_token
from django.conf import settings
from .generator import unique_key_generator



@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request, pk, token):
    """
    Get request.
    activation of your account
    :param request:
    :param user uid:
    :param token generated
    :return: route
    """
    try:
        pkid =force_str(urlsafe_base64_decode(pk))
        user = User.objects.get(pk=pkid)
    except:
        user = None
    print(token)
    if user is not None and account_activation_token.check_token(user, token):

        user.is_active = True
        user.save()
        return Response({'message':"Thank you for your email confirmation. check your password and login to your account ."},status=status.HTTP_202_ACCEPTED)

    else:
        return Response({'message':"Activation link is invalid!"}, status=status.HTTP_202_ACCEPTED)
        




def activateEmail(request, user, to_email):

    """
    Get request.
    send email to user for activation
    :param request:
    :param User object:
    :param email
    :return: mail
    """
    mail_subject = "Activate your Account."
    message = render_to_string("activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(user.username)
    print(to_email)
    email = EmailMessage(subject=mail_subject, body=message,from_email=settings.EMAIL_FROM_USER, to=[to_email])
    if email.send(fail_silently = False):
        return True
    else:
        return False





class NoAuthorizationForPostOnly(IsAuthenticated):

    def has_permission(self, request, view):
        """
        If the request method is POST, then grant permission. Otherwise, authorization is required.
        """
        if request.method == "POST":
            return True
        return super().has_permission(request, view)


class UserAPIView(APIView):
    permission_classes = (NoAuthorizationForPostOnly,)

    def get(self, request):
        user = UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if(type(request.data) == dict):
            json_data = request.data
        else:
            json_data = request.data.dict()
        serializer = UserCreateSerializer(data=json_data)
        if serializer.is_valid():
            user = serializer.save(is_active = False)
            suc = activateEmail(request, user, user.email)
            if suc:
                return Response({'message':f'Dear <b>{user}</b>, please go to you email <b>{user.email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.'}, status=status.HTTP_200_OK)
            return Response({'message':f'Problem sending email to {user.email}, check if you typed it correctly.'}, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
                "messages": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request):
        try:
            if(type(request.data) == dict):
                json_data = request.data
            else:
                json_data = request.data.dict()
            User.objects.filter(id = request.user.id).update(**json_data)
            return Response({"success": True, "message": "update is successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({'success': False, "message": "Unknown Error ocured"}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        request.user.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)
        ...

class UserAllAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)