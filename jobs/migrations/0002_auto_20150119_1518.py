# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='state',
            field=models.CharField(default='CR', choices=[('CR', 'created'), ('AC', 'accepted'), ('RJ', 'rejected')], max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='submission',
            name='token',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
    ]
