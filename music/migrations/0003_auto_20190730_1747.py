# Generated by Django 2.2.3 on 2019-07-30 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_album_song'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.FileField(default=None, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='album',
            name='album_title',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='album',
            name='genre',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='song',
            name='audio_file',
            field=models.FileField(default=None, upload_to='audio/'),
        ),
        migrations.AlterField(
            model_name='song',
            name='song_title',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
