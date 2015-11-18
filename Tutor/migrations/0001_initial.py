# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=2, choices=[(b'M', b'\xe7\x94\xb7'), (b'F', b'\xe5\xa5\xb3')])),
                ('grade', models.CharField(max_length=10, choices=[(b'Primary', b'\xe5\xb0\x8f\xe5\xad\xa6'), (b'J1', b'\xe5\x88\x9d\xe4\xb8\x80'), (b'J2', b'\xe5\x88\x9d\xe4\xba\x8c'), (b'J3', b'\xe5\x88\x9d\xe4\xb8\x89'), (b'H1', b'\xe9\xab\x98\xe4\xb8\x80'), (b'H2', b'\xe9\xab\x98\xe4\xba\x8c'), (b'H3', b'\xe9\xab\x98\xe4\xb8\x89')])),
                ('salary', models.FloatField(null=True, blank=True)),
                ('address', models.CharField(max_length=50, blank=True)),
                ('information', models.CharField(max_length=80, blank=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('userid', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=30, error_messages={b'unique': b'\xe8\xaf\xa5\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe5\xb7\xb2\xe5\xad\x98\xe5\x9c\xa8', b'required': b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba'})),
                ('realname', models.CharField(max_length=30, blank=True)),
                ('password', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('phone', models.CharField(max_length=13, blank=True)),
                ('qq', models.CharField(max_length=13, blank=True)),
                ('gender', models.CharField(max_length=2, choices=[(b'M', b'\xe7\x94\xb7'), (b'F', b'\xe5\xa5\xb3')])),
                ('address', models.CharField(max_length=80, blank=True)),
                ('information', models.CharField(max_length=80, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PTComment',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(related_name='sendecomment', to='Tutor.Parent')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='PTMessage',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(related_name='sendemessage', to='Tutor.Parent')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=10, choices=[(b'Math', b'\xe6\x95\xb0\xe5\xad\xa6'), (b'Chinese', b'\xe8\xaf\xad\xe6\x96\x87'), (b'English', b'\xe8\x8b\xb1\xe8\xaf\xad'), (b'Physic', b'\xe7\x89\xa9\xe7\x90\x86'), (b'Chemistry', b'\xe5\x8c\x96\xe5\xad\xa6'), (b'Biology', b'\xe7\x94\x9f\xe7\x89\xa9')])),
                ('grade', models.CharField(max_length=10, choices=[(b'Primary', b'\xe5\xb0\x8f\xe5\xad\xa6'), (b'J1', b'\xe5\x88\x9d\xe4\xb8\x80'), (b'J2', b'\xe5\x88\x9d\xe4\xba\x8c'), (b'J3', b'\xe5\x88\x9d\xe4\xb8\x89'), (b'H1', b'\xe9\xab\x98\xe4\xb8\x80'), (b'H2', b'\xe9\xab\x98\xe4\xba\x8c'), (b'H3', b'\xe9\xab\x98\xe4\xb8\x89')])),
            ],
        ),
        migrations.CreateModel(
            name='TPComment',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='TPMessage',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('userid', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=30, error_messages={b'unique': b'\xe8\xaf\xa5\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe5\xb7\xb2\xe5\xad\x98\xe5\x9c\xa8', b'required': b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba'})),
                ('password', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('gender', models.CharField(default=b'M', max_length=2, choices=[(b'M', b'\xe7\x94\xb7'), (b'F', b'\xe5\xa5\xb3')])),
                ('state', models.CharField(default=b'F', max_length=2, choices=[(b'B', b'\xe5\xbf\x99\xe7\xa2\x8c'), (b'F', b'\xe7\xa9\xba\xe9\x97\xb2')])),
                ('realname', models.CharField(max_length=30, blank=True)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('phone', models.CharField(max_length=13, blank=True)),
                ('qq', models.CharField(max_length=13, blank=True)),
                ('university', models.CharField(max_length=30, blank=True)),
                ('major', models.CharField(max_length=40, blank=True)),
                ('information', models.CharField(max_length=80, blank=True)),
                ('subject', models.ManyToManyField(to='Tutor.Subject', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='tpmessage',
            name='from_user',
            field=models.ForeignKey(related_name='sendemessage', to='Tutor.Tutor'),
        ),
        migrations.AddField(
            model_name='tpmessage',
            name='to_user',
            field=models.ForeignKey(related_name='receivemessage', to='Tutor.Parent'),
        ),
        migrations.AddField(
            model_name='tpcomment',
            name='from_user',
            field=models.ForeignKey(related_name='sendecomment', to='Tutor.Tutor'),
        ),
        migrations.AddField(
            model_name='tpcomment',
            name='to_user',
            field=models.ForeignKey(related_name='receivecomment', to='Tutor.Parent'),
        ),
        migrations.AddField(
            model_name='ptmessage',
            name='to_user',
            field=models.ForeignKey(related_name='receivemessage', to='Tutor.Tutor'),
        ),
        migrations.AddField(
            model_name='ptcomment',
            name='to_user',
            field=models.ForeignKey(related_name='receivecomment', to='Tutor.Tutor'),
        ),
        migrations.AddField(
            model_name='employ',
            name='parent',
            field=models.ForeignKey(to='Tutor.Parent'),
        ),
        migrations.AddField(
            model_name='employ',
            name='subject',
            field=models.ManyToManyField(to='Tutor.Subject'),
        ),
    ]
