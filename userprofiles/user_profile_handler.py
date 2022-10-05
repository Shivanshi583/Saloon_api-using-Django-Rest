from os import access
import uuid
from userprofiles.models import Profiles
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import RefreshToken



class UserProfileHandler():
    def generate_profile_response(self, userprofile):
        return {
            'uuid': userprofile.uuid,
            'name': userprofile.name,
            'username': userprofile.user.username,
            'email': userprofile.email,
            'profile_type': userprofile.profile_type,
            'dob': userprofile.dob,
            'gender': userprofile.gender,
            'created_at': userprofile.created_at,
            'updated_at': userprofile.updated_at,
            'is_deleted': userprofile.is_deleted
        }   

    def create_profile(
        self, username, first_name, last_name, email, password, profile_type, dob, gender): 

        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()

        profile = Profiles.objects.create(
            user = user,
            name = user.first_name + ' ' + user.last_name,
            email = user.email,
            profile_type = profile_type,
            dob = dob,
            gender = gender
        )

        return {
            'success': True,
            'user_profile': self.generate_profile_response(profile)
        }


    def update_profile(
        self, user, first_name, last_name, profile_type, dob, gender):


        import ipdb;
        ipdb.set_trace()
        
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