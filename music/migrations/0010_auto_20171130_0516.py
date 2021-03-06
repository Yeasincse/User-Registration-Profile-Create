# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-30 05:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0009_auto_20171130_0445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=250)),
                ('post_title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=100)),
                ('post_logo', models.FileField(upload_to='')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='album',
            name='user',
        ),
        migrations.DeleteModel(
            name='Album',
        ),
    ]
