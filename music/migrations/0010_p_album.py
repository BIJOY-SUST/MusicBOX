# Generated by Django 2.2.3 on 2019-08-03 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_auto_20190802_1827'),
    ]

    operations = [
        migrations.CreateModel(
            name='P_Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(default=None, max_length=20)),
                ('album_title', models.CharField(default=None, max_length=20)),
                ('genre', models.CharField(default=None, max_length=20)),
                ('album_logo', models.FileField(default=None, upload_to='images/')),
                ('is_favorite', models.BooleanField(default=False)),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
