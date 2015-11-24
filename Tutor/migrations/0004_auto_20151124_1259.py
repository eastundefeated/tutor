# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0003_auto_20151124_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exp',
            name='title',
            field=models.CharField(max_length=20, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', error_messages={b'required': b'\xe6\xa0\x87\xe9\xa2\x98\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba'}),
        ),
    ]
