# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aws', '0002_auto_20150406_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='awskey',
            field=models.TextField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='awssecret',
            field=models.TextField(max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
