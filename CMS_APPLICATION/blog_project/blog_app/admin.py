from django.contrib import admin

from .models import Blog, LikeBlog

# Register your models here.


class BlogAdmin(admin.ModelAdmin):

    list_display = ['id','title', 'description', 'content',
                    'created_date', 'is_active', 'is_private']
    list_filter = ['title', 'description', 'content',
                   'created_date', 'is_active', 'is_private']
    search_fields = ['title', 'description', 'content',
                     'created_date', 'is_active', 'is_private']
    ordering = ['created_date']


class LikeBlogAdmin(admin.ModelAdmin):

    list_display = ['id','like', 'blog', 'created_by', 'is_active']


admin.site.register(Blog, BlogAdmin)
admin.site.register(LikeBlog, LikeBlogAdmin)
