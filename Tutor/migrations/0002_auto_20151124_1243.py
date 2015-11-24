# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exp',
            name='content',
            field=models.TextField(verbose_name=b'\xe5\x86\x85\xe5\xae\xb9', blank=True),
        ),
    ]
