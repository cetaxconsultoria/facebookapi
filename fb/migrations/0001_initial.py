# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-06 21:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField()),
                ('social_id', models.TextField(unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('expires', models.IntegerField()),
                ('scope', models.CharField(max_length=1000)),
                ('first_name', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=150)),
                ('thumbnail', models.CharField(max_length=1000, null=True)),
                ('thumbnail_age', models.DateTimeField(null=True)),
                ('link', models.URLField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
