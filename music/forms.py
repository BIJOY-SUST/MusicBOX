from django import forms
from django.contrib.auth.models import User,AbstractUser

from .models import Album, Song,CustomUser


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(max_length=200,help_text='Required')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']