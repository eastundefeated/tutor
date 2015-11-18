# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0003_employ_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='employ',
            name='info3',
            field=models.CharField(max_length=2, blank=True),
        ),
    ]
