# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 20:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0002_logentry_remove_auto_add'),
        ('authtoken', '0001_initial'),
        ('board', '0003_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_ptr',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]