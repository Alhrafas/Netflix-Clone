from django.contrib import admin
from .models import  Movies, Profile, CustomUser,Videos
# Register your models here.
admin.site.register(Movies)
admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Videos)