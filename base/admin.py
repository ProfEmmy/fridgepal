from django.contrib import admin
from .models import UsersGroup, Group, Classification, Item

# Register your models here.
admin.site.register(UsersGroup)
admin.site.register(Group)
admin.site.register(Classification)
admin.site.register(Item)