# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FindTeammates', '0002_auto_20150510_0334'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='headline',
            field=models.CharField(default='Columbia University student', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='image',
            field=models.CharField(default=' ', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='skill',
            field=models.CharField(default='Java, C', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='url',
            field=models.CharField(default='http://www.linkedin.com', max_length=1000),
            preserve_default=False,
        ),
    ]
