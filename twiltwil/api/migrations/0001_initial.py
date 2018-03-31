# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-31 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sid', models.CharField(max_length=255, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sid', models.CharField(max_length=255, unique=True)),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('channel', models.CharField(choices=[('sms', 'SMS')], db_index=True, max_length=15)),
                ('sender', models.CharField(max_length=255)),
                ('recipient', models.CharField(max_length=255)),
                ('direction', models.CharField(choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')], db_index=True, max_length=8)),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('queued', 'Queued'), ('sending', 'Sending'), ('sent', 'Sent'), ('receiving', 'Receiving'), ('received', 'Received'), ('delivered', 'Delivered'), ('undelivered', 'Undelivered'), ('failed', 'Failed')], max_length=15)),
                ('text', models.TextField(blank=True)),
                ('addons', models.TextField(blank=True, null=True)),
                ('raw', models.TextField(blank=True, null=True)),
                ('task_sid', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('worker_sid', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('resolved', models.BooleanField(db_index=True, default=False)),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
    ]
