# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2019-05-01 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pvp', '0002_auto_20150506_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle1x1',
            name='matchmaker_battle_id',
            field=models.BigIntegerField(null=True),
        ),
    ]