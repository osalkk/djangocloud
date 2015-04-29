# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws', '0004_auto_20150421_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='awsaction',
            name='days',
            field=models.TextField(max_length=200, blank=True),
            preserve_default=True,
        ),
    ]
