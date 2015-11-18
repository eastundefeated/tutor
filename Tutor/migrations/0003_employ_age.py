# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0002_auto_20151108_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='employ',
            name='age',
            field=models.CharField(default=b'', max_length=2, choices=[(b'0', b'5\xe5\xb2\x81\xe4\xbb\xa5\xe4\xb8\x8b'), (b'1', b'5\xe5\xb2\x81\xe8\x87\xb312\xe5\xb2\x81'), (b'2', b'12\xe8\x87\xb316\xe5\xb2\x81'), (b'3', b'16\xe5\xb2\x81\xe4\xbb\xa5\xe4\xb8\x8a')]),
        ),
    ]
