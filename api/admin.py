from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(ApplicationUser)
admin.site.register(FriendRequest)
admin.site.register(UserLoginData)