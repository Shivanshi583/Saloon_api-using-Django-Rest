import email
from rest_framework.views import APIView
from rest_framework import status as status_codes
from django.http import JsonResponse

from userprofiles.user_profile_handler import UserProfileHandler

from rest_framework.permissions import IsAuthenticated, AllowAny


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from django.contrib.auth.models import User


class ProfileView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        profile_type = request.data.get('profile_type')
        dob = request.data.get('dob')
        gender = request.data.get('gender')

        userprofile_handler = UserProfileHandler()
        response = userprofile_handler.create_profile(  
            username, first_name, last_name, email, 
            password, profile_type, dob, gender)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)

class ProfileAuthView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user

        userprofile_handler = UserProfileHandler()
        response = userprofile_handler.get_profile(user)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        profile_type = request.data.get('profile_type')
        dob = request.data.get('dob')
        gender = request.data.get('gender')

        userprofile_handler = UserProfileHandler()
        response = userprofile_handler.update_profile(
            user, first_name, last_name, profile_type, dob, gender)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class ProfileIdView(APIView):

   

    def get(self, request, *args, **kwargs):
        user = request.user

        userprofile_handler = UserProfileHandler()
        response = userprofile_handler.get_profile(user)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        user = request.user
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        profile_type = request.data.get('profile_type')
        dob = request.data.get('dob')
        gender = request.data.get('gender')

        userprofile_handler = UserProfileHandler()
        response = userprofile_handler.update_profile(
            user, first_name, last_name, profile_type, dob, gender)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        user = request.user

        userprofile_handler = UserProfileHandler()
        response = userprofile_handler.delete_profile_by_id(user)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)



class ProfileLoginView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        userprofile_handler = UserProfileHandler()
        response = userprofile_handler.get_login_profile_details(
            username, password)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)