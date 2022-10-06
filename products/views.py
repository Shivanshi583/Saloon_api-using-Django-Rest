import email
from rest_framework.views import APIView
from rest_framework import status as status_codes
from django.http import JsonResponse
from products.product_handler import ProductHandler

from userprofiles.user_profile_handler import UserProfileHandler

from rest_framework.permissions import IsAuthenticated, AllowAny


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)


class ProductView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        name = request.data.get('name')
        description = request.data.get('description')
        price = request.data.get('price')
        brand = request.data.get('brand')
        rating = request.data.get('rating')

        product_handler = ProductHandler()
        response = product_handler.create_product(  
            user, name, description, price, 
            brand, rating)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        product_handler = ProductHandler()
        response = product_handler.get_all_products(  
            user)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)


class ProductIdView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        product_handler = ProductHandler()
        response = product_handler.get_product_by_id(  
            product_id)

        return JsonResponse(response, status=status_codes.HTTP_200_OK)
