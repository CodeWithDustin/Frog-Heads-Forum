from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
  username = models.OneToOneField(User, related_name='profile' ,on_delete=models.CASCADE)
  profile_img = models.ImageField(upload_to='media', default='images/blank_image.png')
  bio = models.TextField(blank=True)
  location = models.CharField(max_length=50, blank=True)

  def __str__(self):
    return f"{self.username.username}'s Profile"
  
class MessageBoard(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(blank = True)
  date_created = models.DateTimeField(default=datetime.now)

  def __str__(self):
    return self.title


class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.Case)
  board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE)
  subject = models.CharField(max_length=100, blank=True, null=True)
  post = models.CharField(max_length=300)
  post_img = models.ImageField(upload_to='media', blank=True)
  date_posted = models.DateField(default=datetime.now)

  def __str__(self):
    return f"{self.user.username}'s Post on {self.board.title}"
  
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    reply = models.TextField()
    date_replied = models.DateField(default=datetime.now)

  