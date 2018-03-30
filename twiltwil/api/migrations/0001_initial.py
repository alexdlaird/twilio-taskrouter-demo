# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-29 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sid', models.CharField(max_length=255)),
                ('channel', models.CharField(choices=[('sms', 'SMS')], max_length=15)),
                ('sender', models.CharField(max_length=255)),
                ('receiver', models.CharField(max_length=255)),
                ('direction', models.CharField(choices=[('inbound', 'Inbound'), ('outbound', 'Outbound')], max_length=8)),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('queued', 'Queued'), ('sending', 'Sending'), ('sent', 'Sent'), ('receiving', 'Receiving'), ('received', 'Received'), ('delivered', 'Delivered'), ('undelivered', 'Undelivered'), ('failed', 'Failed')], max_length=15)),
                ('text', models.TextField(blank=True)),
                ('addons', models.TextField(blank=True, null=True)),
                ('raw', models.TextField(blank=True, null=True)),
                ('task_sid', models.CharField(blank=True, max_length=255, null=True)),
                ('worker_sid', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
