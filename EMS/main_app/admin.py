from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(Staff)
admin.site.register(Client)
admin.site.register(Department)
admin.site.register(Project)
admin.site.register(Timeline)
