#encoding:utf-8
from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
#在ADMIN后台显示该表，并提供默认的增删改查功能
from .models import Admin

class Admin1(admin.ModelAdmin):
    list_display = ('user','password')

admin.site.register(Admin)