from django.contrib import admin
from .models import User, Post


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)


class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Post, PostAdmin)
