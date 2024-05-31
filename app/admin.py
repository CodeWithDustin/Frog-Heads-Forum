from django.contrib import admin

from app.models import Profile, MessageBoard, Post

# Register your models here.
admin.site.register(Profile)
admin.site.register(MessageBoard)
admin.site.register(Post)