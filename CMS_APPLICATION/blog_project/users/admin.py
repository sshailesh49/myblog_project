from django.contrib import admin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    class meta:
        model =CustomUser
        list_display = ('first_name','phone','email', 'is_staff', 'is_active',)
        list_filter = ('email', 'is_staff', 'is_active','phone')
     
        search_fields = ('email',)
        ordering = ('email',)
        


admin.site.register(CustomUser, CustomUserAdmin)