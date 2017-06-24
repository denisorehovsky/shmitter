# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-24 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=140, verbose_name='body')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
            ],
            options={
                'verbose_name': 'tweet',
                'verbose_name_plural': 'tweets',
                'ordering': ['-created'],
            },
        ),
    ]
