# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300, blank=True)),
                ('job_file', models.FileField(upload_to='')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('token', django_extensions.db.fields.UUIDField(editable=False, blank=True, name='token')),
                ('submit_file', models.FileField(upload_to='')),
                ('state', models.CharField(max_length=2, choices=[('CR', 'created'), ('AC', 'accepted'), ('RJ', 'rejected')])),
                ('rating', models.IntegerField(max_length=1, blank=True, null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('job', models.ForeignKey(to='jobs.Job')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
