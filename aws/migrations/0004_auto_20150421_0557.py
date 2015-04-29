# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aws', '0003_auto_20150407_1110'),
    ]

    operations = [
        migrations.AddField(
            model_name='awsaction',
            name='days',
            field=models.CharField(max_length=200, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awsaction',
            name='recurring',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='awsaction',
            name='user',
            field=models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='awsaction',
            name='weeks',
            field=models.IntegerField(default=1, blank=True),
            preserve_default=False,
        ),
    ]
