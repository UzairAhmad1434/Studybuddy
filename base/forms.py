from django import forms
from .models import Room,User
# from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']