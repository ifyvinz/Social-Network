from django.contrib import admin
from .models import User, Profile, Post, Relationship
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Relationship)