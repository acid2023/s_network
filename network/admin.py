from django.contrib import admin

from network.models import SocialUser, Post, Attitude, Comment
# Register your models here.


@admin.register(SocialUser)
class SocialUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'date_of_birth', 'avatar', 'username', 'password')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at')


@admin.register(Attitude)
class AttitudeAdmin(admin.ModelAdmin):
    list_display = ('author', 'liked_in', 'created_at', 'like')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'author', 'created_at', 'posted_in')

