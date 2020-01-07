from django.contrib import admin
from api.models import UserProfile, Followers

admin.site.register(UserProfile)
admin.site.register(Followers)