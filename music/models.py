from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # nick_name =  models.CharField(null=True,blank=True,default=None,max_length=20)
    # add additional fields in here

    def __str__(self):
        return self.email


class FeebBack(models.Model):
    feedback_id = models.AutoField(null=False,blank=False,default=None, primary_key=True)
    email = models.EmailField(null=False,blank=False,default=None)
    name = models.CharField(null=False,blank=False,default=None,max_length=20)
    mobile_no = models.CharField(null=False,blank=False,default=None,max_length=20)
    tmessage = models.TextField(null=False,blank=False,default=None)
    def __str__(self):
        return self.email

class Album(models.Model):
    user = models.ForeignKey(CustomUser, default=1,on_delete=models.CASCADE)
    artist = models.CharField(null=False,blank=False,default=None,max_length=20)
    album_title = models.CharField(null=False,blank=False,default=None,max_length=20)
    genre = models.CharField(null=False,blank=False,default=None,max_length=20)
    album_logo = models.FileField(null=False,blank=False,default=None,upload_to='images/')
    is_favorite = models.BooleanField(null=False,blank=False,default=False)


    def __str__(self):
        return self.album_title+' - '+self.artist

class P_Album(models.Model):
    user = models.ForeignKey(CustomUser, default=1,on_delete=models.CASCADE)
    original = models.ForeignKey(Album, default=1,on_delete=models.CASCADE)
    artist = models.CharField(null=False,blank=False,default=None,max_length=20)
    album_title = models.CharField(null=False,blank=False,default=None,max_length=20)
    genre = models.CharField(null=False,blank=False,default=None,max_length=20)
    album_logo = models.FileField(null=False,blank=False,default=None,upload_to='images/')
    is_favorite = models.BooleanField(null=False,blank=False,default=False)


    def __str__(self):
        return self.album_title+' - '+self.artist



class Song(models.Model):
    user = models.ForeignKey(CustomUser, default=1,on_delete=models.CASCADE)
    album = models.ForeignKey(Album, default=1,on_delete=models.CASCADE)
    song_title =  models.CharField(null=False,blank=False,default=None,max_length=20)
    audio_file = models.FileField(null=False,blank=False,default=None,upload_to='audio/')
    is_favorite = models.BooleanField(null=False,blank=False,default=False)

    def __str__(self):
        return self.song_title