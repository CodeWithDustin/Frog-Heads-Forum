from django import forms

from app.models import *



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['profile_img', 'bio', 'location']


class BoardForm(forms.ModelForm):
    
    class Meta:
        model = MessageBoard
        fields = ['title', 'description']

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['subject', 'post', 'post_img']