from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, ProfileForm
from .models import CustomUser, Post
from taggit.models import Tag
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = ProfileForm
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'profile_picture', 'bio']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_picture', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('profile_picture', 'bio')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Register the Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('published_date', 'author')

