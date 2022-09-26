from django.urls import path
from userprofiles.views import (
    ProfileView,
    ProfileIdView
)           



urlpatterns = [
    path('profiles/', ProfileView.as_view(), name="userprofile_create"),
    path('profile/', ProfileIdView.as_view(), name="userprofile_get_update_delete"),
]       