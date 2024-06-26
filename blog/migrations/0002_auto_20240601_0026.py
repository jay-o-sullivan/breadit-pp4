# Generated by Django 3.2.25 on 2024-06-01 00:26

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
     
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
        migrations.AddField(
            model_name='post',
            name='downvotes',
            field=models.ManyToManyField(blank=True, related_name='post_downvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='upvotes',
            field=models.ManyToManyField(blank=True, related_name='post_upvotes', to=settings.AUTH_USER_MODEL),
        ),
        
    
    ]
