# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0004_employ_info3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employ',
            name='grade',
            field=models.CharField(default=b'', max_length=10, choices=[(b'Primary', ((b'P1', b'\xe5\xb0\x8f\xe5\xad\xa6\xe4\xb8\x80\xe5\xb9\xb4\xe7\xba\xa7'), (b'P2', b'\xe5\xb0\x8f\xe5\xad\xa6\xe4\xba\x8c\xe5\xb9\xb4\xe7\xba\xa7'))), (b'J1', b'\xe5\x88\x9d\xe4\xb8\x80'), (b'J2', b'\xe5\x88\x9d\xe4\xba\x8c'), (b'J3', b'\xe5\x88\x9d\xe4\xb8\x89'), (b'H1', b'\xe9\xab\x98\xe4\xb8\x80'), (b'H2', b'\xe9\xab\x98\xe4\xba\x8c'), (b'H3', b'\xe9\xab\x98\xe4\xb8\x89')]),
        ),
        migrations.AlterField(
            model_name='subject',
            name='grade',
            field=models.CharField(max_length=10, choices=[(b'Primary', ((b'P1', b'\xe5\xb0\x8f\xe5\xad\xa6\xe4\xb8\x80\xe5\xb9\xb4\xe7\xba\xa7'), (b'P2', b'\xe5\xb0\x8f\xe5\xad\xa6\xe4\xba\x8c\xe5\xb9\xb4\xe7\xba\xa7'))), (b'J1', b'\xe5\x88\x9d\xe4\xb8\x80'), (b'J2', b'\xe5\x88\x9d\xe4\xba\x8c'), (b'J3', b'\xe5\x88\x9d\xe4\xb8\x89'), (b'H1', b'\xe9\xab\x98\xe4\xb8\x80'), (b'H2', b'\xe9\xab\x98\xe4\xba\x8c'), (b'H3', b'\xe9\xab\x98\xe4\xb8\x89')]),
        ),
    ]
