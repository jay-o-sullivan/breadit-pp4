from django import forms
from .models import Comment, Post, Profile

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'featured_image', 'excerpt', 'content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']
