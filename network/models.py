from django.db import models
from django.contrib.auth.models import User


class SocialUser(User):
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)


class Post(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=100)
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_in = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


class Attitude(models.Model):
    author = models.ForeignKey(SocialUser, on_delete=models.CASCADE)
    liked_in = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    like = models.BooleanField(default=True)



    
