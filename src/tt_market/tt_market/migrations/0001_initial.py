# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-10-13 16:24
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogRecord',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('operation_type', models.IntegerField()),
                ('lot_type', models.IntegerField()),
                ('item_type', models.CharField(max_length=32)),
                ('item', models.UUIDField()),
                ('owner', models.BigIntegerField(null=True)),
                ('price', models.IntegerField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default='{}')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'db_table': 'log_records',
            },
        ),
        migrations.CreateModel(
            name='SellLot',
            fields=[
                ('item_type', models.CharField(max_length=32)),
                ('item', models.UUIDField(primary_key=True, serialize=False)),
                ('price', models.IntegerField()),
                ('owner', models.BigIntegerField(db_index=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'sell_lots',
            },
        ),
        migrations.AlterIndexTogether(
            name='selllot',
            index_together=set([('item_type', 'price')]),
        ),
        migrations.AlterIndexTogether(
            name='logrecord',
            index_together=set([('operation_type', 'created_at')]),
        ),
    ]
