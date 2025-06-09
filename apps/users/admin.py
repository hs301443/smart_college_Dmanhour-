
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Graduation,Staff

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
 



class GraduationAdmin(admin.ModelAdmin):
    list_display = [ 'employment_status', 'job_name']


admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Graduation, GraduationAdmin)

admin.site.register(Staff)