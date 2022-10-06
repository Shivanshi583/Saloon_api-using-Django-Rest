from math import prod
from os import access
import profile
import uuid
from products.models import Product
from userprofiles.models import Profiles
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import RefreshToken



class ProductHandler():
    def generate_product_response(self, product):
        return {
            'uuid': product.uuid,
            'name': product.name,
            'vendor':{
                'uuid': product.vendor.uuid,
                'name': product.vendor.name,
                'email': product.vendor.email
            },
            'description': product.description,
            'price': product.price,
            'brand': product.brand,
            'rating': product.rating,
            'created_at': product.created_at,
            'updated_at': product.updated_at,
            'is_deleted': product.is_deleted
        }   

    def create_product(
        self, user, name, description, price, brand, rating): 

        vendor = Profiles.objects.get(user= user)
        
        product = Product.objects.create(
            vendor = vendor,
            name = name,
            description = description,
            price = price,
            brand = brand,
            rating = rating
        )

        return {
            'success': True,
            'product_details': self.generate_product_response(product)
        }



    def get_all_products(self, user): 

        profile = Profiles.objects.get(
            user=user)

        if profile.profile_type == 'VENDOR':
            products = Product.objects.filter(vendor = profile) #(vendor__user = user) vendor__user__username=user.username
        else:
            products = Product.objects.all()

        return {
            'success': True,
            'products': [self.generate_product_response(product) for product in products]
        }

    def get_product_by_id(self, product_id): 

        product = Product.objects.filter(pk=product_id).first()

        return {
            'success': True,
            'product': self.generate_product_response(product)
        }


    def update_profile(
        self, user, first_name, last_name, profile_type, dob, gender):

        profile = Profiles.objects.get(user= user)

        if first_name:
            profile.user.first_name = first_name
        if last_name:
            profile.user.last_name = last_name
        if profile_type:
            profile.profile_type = profile_type
        if dob:
            profile.dob = dob
        if gender:
            profile.gender = gender
        profile.user.save()
        profile.name = profile.user.first_name + ' ' + profile.user.last_name
        
        profile.save()
        
        # profile.update(
        #     name = name,
        #     profile_type = profile_type,
        #     dob = dob,
        #     gender = gender
        # )

        return {
            'success': True,
            'user_profile': self.generate_profile_response(profile)
        }


    
    def get_all_profiles(self):

        profiles = Profiles.objects.filter(is_deleted = False)

        return {
            'success': True,
            'user_profiles':[self.generate_profile_response(profile) for profile in profiles] 
        }
    
    def get_profile_by_id(self, profile_id):

        profile = Profiles.objects.filter(uuid=profile_id, is_deleted = False).first() #can also use pk
        
        return {
            'success': True,
            'user_profile':self.generate_profile_response(profile) if profile else "Does not exist"     
        }
    
    def get_profile(self, user):

        profile = Profiles.objects.get(user=user) #can also use pk
        
        return {
            'success': True,
            'user_profile':self.generate_profile_response(profile) if profile else "Does not exist"     
        }

    def delete_profile(self, profile_id,user):

        profile = Profiles.objects.get(user=user)
        profile.is_deleted = True # to actually delete use profile.delete()
        profile.save()
        
        return {
            'success': True
        }

    
    def get_login_profile_details(self, username, password):
        profile = Profiles.objects.get(user__username=username)
        if profile.user.check_password(password):
            tokens = RefreshToken.for_user(profile.user)
            refresh = str(tokens)
            access = str(tokens.access_token)
            profile_data = self.generate_profile_response(profile)

            return {
                'success': True,
                'refresh': refresh,
                'access': access,
                'profile': profile_data
            }
        else:
            return {
                'success': False,
                'message': 'Either user doesnt exist or username and password doesnt match'
            }