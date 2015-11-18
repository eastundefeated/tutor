# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tutor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employ',
            old_name='gender',
            new_name='gender1',
        ),
        migrations.RemoveField(
            model_name='employ',
            name='address',
        ),
        migrations.RemoveField(
            model_name='employ',
            name='information',
        ),
        migrations.AddField(
            model_name='employ',
            name='gender2',
            field=models.CharField(default=b'N', max_length=2, choices=[(b'N', b'\xe7\x94\xb7\xe5\xa5\xb3\xe4\xb8\x8d\xe9\x99\x90'), (b'M', b'\xe7\x94\xb7'), (b'F', b'\xe5\xa5\xb3')]),
        ),
        migrations.AddField(
            model_name='employ',
            name='info1',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='employ',
            name='info2',
            field=models.CharField(max_length=2, blank=True),
        ),
        migrations.AddField(
            model_name='employ',
            name='linkman',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='employ',
            name='phone',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='employ',
            name='site',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='employ',
            name='time',
            field=models.CharField(max_length=15, blank=True),
        ),
        migrations.AddField(
            model_name='employ',
            name='way',
            field=models.CharField(default=b'', max_length=2, choices=[(b'S', b'\xe5\xad\xa6\xe7\x94\x9f\xe4\xb8\x8a\xe9\x97\xa8'), (b'T', b'\xe5\xae\xb6\xe6\x95\x99\xe4\xb8\x8a\xe9\x97\xa8')]),
        ),
        migrations.AlterField(
            model_name='employ',
            name='grade',
            field=models.CharField(default=b'', max_length=10, choices=[(b'Primary', b'\xe5\xb0\x8f\xe5\xad\xa6'), (b'J1', b'\xe5\x88\x9d\xe4\xb8\x80'), (b'J2', b'\xe5\x88\x9d\xe4\xba\x8c'), (b'J3', b'\xe5\x88\x9d\xe4\xb8\x89'), (b'H1', b'\xe9\xab\x98\xe4\xb8\x80'), (b'H2', b'\xe9\xab\x98\xe4\xba\x8c'), (b'H3', b'\xe9\xab\x98\xe4\xb8\x89')]),
        ),
        migrations.RemoveField(
            model_name='employ',
            name='subject',
        ),
        migrations.AddField(
            model_name='employ',
            name='subject',
            field=models.CharField(default=b'', max_length=10, choices=[(b'Math', b'\xe6\x95\xb0\xe5\xad\xa6'), (b'Chinese', b'\xe8\xaf\xad\xe6\x96\x87'), (b'English', b'\xe8\x8b\xb1\xe8\xaf\xad'), (b'Physic', b'\xe7\x89\xa9\xe7\x90\x86'), (b'Chemistry', b'\xe5\x8c\x96\xe5\xad\xa6'), (b'Biology', b'\xe7\x94\x9f\xe7\x89\xa9')]),
        ),
    ]
