from django.contrib import admin
from .models import CASLPermission
from .models import UserPermission

# Register your models here.
admin.site.register(CASLPermission)
admin.site.register(UserPermission)
