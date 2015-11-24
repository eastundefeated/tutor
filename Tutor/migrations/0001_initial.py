# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseMessage',
            fields=[
                ('ID', models.AutoField(serialize=False, primary_key=True)),
                ('content', models.TextField(blank=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='BaseProfile',
            fields=[
                ('userid', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=30, verbose_name=b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d', error_messages={b'unique': b'\xe8\xaf\xa5\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe5\xb7\xb2\xe5\xad\x98\xe5\x9c\xa8', b'required': b'\xe7\x94\xa8\xe6\x88\xb7\xe5\x90\x8d\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba'})),
                ('realname', models.CharField(max_length=30, verbose_name=b'\xe7\x9c\x9f\xe5\xae\x9e\xe5\xa7\x93\xe5\x90\x8d', blank=True)),
                ('password', models.CharField(max_length=30, error_messages={b'required': b'\xe5\xaf\x86\xe7\xa0\x81\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba'})),
                ('email', models.EmailField(max_length=254, verbose_name=b'\xe7\x94\xb5\xe5\xad\x90\xe9\x82\xae\xe7\xae\xb1', error_messages={b'required': b'\xe9\x82\xae\xe7\xae\xb1\xe4\xb8\x8d\xe8\x83\xbd\xe4\xb8\xba\xe7\xa9\xba', b'invalid': b'\xe8\xaf\xb7\xe8\xbe\x93\xe5\x85\xa5\xe6\xa0\xb8\xe5\xaf\xb9\xe9\x82\xae\xe7\xae\xb1\xe6\xa0\xbc\xe5\xbc\x8f'})),
                ('gender', models.CharField(default=b'M', max_length=2, verbose_name=b'\xe6\x80\xa7\xe5\x88\xab', choices=[(b'M', b'\xe7\x94\xb7'), (b'F', b'\xe5\xa5\xb3')])),
                ('age', models.IntegerField(null=True, verbose_name=b'\xe5\xb9\xb4\xe9\xbe\x84', blank=True)),
                ('phone', models.CharField(max_length=13, verbose_name=b'\xe7\x94\xb5\xe8\xaf\x9d', blank=True)),
                ('qq', models.CharField(max_length=13, verbose_name=b'QQ', blank=True)),
                ('information', models.TextField(verbose_name=b'\xe8\xa1\xa5\xe5\x85\x85\xe4\xbf\xa1\xe6\x81\xaf', blank=True)),
            ],
            options={
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='Employ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('age', models.CharField(default=b'3', max_length=2, verbose_name=b'\xe5\xad\x90\xe5\xa5\xb3\xe5\xb9\xb4\xe9\xbe\x84', choices=[(b'0', b'5\xe5\xb2\x81\xe4\xbb\xa5\xe4\xb8\x8b'), (b'1', b'5\xe5\xb2\x81\xe8\x87\xb312\xe5\xb2\x81'), (b'2', b'12\xe8\x87\xb316\xe5\xb2\x81'), (b'3', b'16\xe5\xb2\x81\xe4\xbb\xa5\xe4\xb8\x8a')])),
                ('gender1', models.CharField(default=b'M', max_length=2, verbose_name=b'\xe5\xad\x90\xe5\xa5\xb3\xe6\x80\xa7\xe5\x88\xab', choices=[(b'M', b'\xe7\x94\xb7'), (b'F', b'\xe5\xa5\xb3')])),
                ('info1', models.TextField(verbose_name=b'\xe5\xad\x90\xe5\xa5\xb3\xe9\xa2\x9d\xe5\xa4\x96\xe4\xbf\xa1\xe6\x81\xaf\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('gender2', models.CharField(default=b'N', max_length=2, verbose_name=b'\xe5\xae\xb6\xe6\x95\x99\xe6\x80\xa7\xe5\x88\xab\xe8\xa6\x81\xe6\xb1\x82', choices=[(b'N', b'\xe7\x94\xb7\xe5\xa5\xb3\xe4\xb8\x8d\xe9\x99\x90'), (b'M', b'\xe7\x94\xb7'), (b'F', b'\xe5\xa5\xb3')])),
                ('site', models.CharField(default=b'home', max_length=10, verbose_name=b'\xe6\x95\x99\xe5\xad\xa6\xe5\x9c\xb0\xe7\x82\xb9', choices=[(b'home', b'\xe5\xae\xb6\xe6\x95\x99\xe4\xb8\x8a\xe9\x97\xa8'), (b'school', b'\xe5\xad\xa6\xe7\x94\x9f\xe4\xb8\x8a\xe9\x97\xa8')])),
                ('time', models.CharField(default=b'8-11', max_length=10, verbose_name=b'\xe6\x95\x99\xe5\xad\xa6\xe6\x97\xb6\xe9\x97\xb4\xe6\xae\xb5', choices=[(b'8-11', b'8:00-11:30'), (b'14-17', b'14:00-17:30'), (b'19-21', b'19:00-21:30')])),
                ('info2', models.TextField(verbose_name=b'\xe5\xae\xb6\xe6\x95\x99\xe9\xa2\x9d\xe5\xa4\x96\xe8\xa6\x81\xe6\xb1\x82', blank=True)),
                ('salary', models.FloatField(null=True, verbose_name=b'\xe8\x96\xaa\xe6\xb0\xb4(\xe5\x85\x83/\xe5\xb0\x8f\xe6\x97\xb6)', blank=True)),
                ('info3', models.TextField(verbose_name=b'\xe8\xa1\xa5\xe5\x85\x85\xe8\xaf\xb4\xe6\x98\x8e', blank=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('valid_days', models.IntegerField(default=30, verbose_name=b'\xe8\xa1\xa8\xe5\x8d\x95\xe6\x9c\x89\xe6\x95\x88\xe6\x9c\x9f(\xe5\xa4\xa9)')),
            ],
            options={
                'ordering': ['-pub_date', 'salary'],
            },
        ),
        migrations.CreateModel(
            name='Exp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=20, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98', blank=True)),
                ('content', models.TextField(verbose_name=b'\xe5\x86\x85\xe5\xae\xb9')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
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
                ('grade', models.CharField(max_length=10, choices=[(b'Pr', b'\xe5\xb0\x8f\xe5\xad\xa6'), (b'J1', b'\xe5\x88\x9d\xe4\xb8\x80'), (b'J2', b'\xe5\x88\x9d\xe4\xba\x8c'), (b'J3', b'\xe5\x88\x9d\xe4\xb8\x89'), (b'H1', b'\xe9\xab\x98\xe4\xb8\x80'), (b'H2', b'\xe9\xab\x98\xe4\xba\x8c'), (b'H3', b'\xe9\xab\x98\xe4\xb8\x89')])),
            ],
            options={
                'ordering': ['grade', 'subject'],
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('baseprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Tutor.BaseProfile')),
                ('address', models.TextField(verbose_name=b'\xe5\x9c\xb0\xe5\x9d\x80', blank=True)),
            ],
            bases=('Tutor.baseprofile',),
        ),
        migrations.CreateModel(
            name='PTComment',
            fields=[
                ('basemessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Tutor.BaseMessage')),
                ('from_user', models.ForeignKey(related_name='sendecomment', to='Tutor.Parent')),
            ],
            bases=('Tutor.basemessage',),
        ),
        migrations.CreateModel(
            name='PTMessage',
            fields=[
                ('basemessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Tutor.BaseMessage')),
                ('from_user', models.ForeignKey(related_name='sendemessage', to='Tutor.Parent')),
            ],
            bases=('Tutor.basemessage',),
        ),
        migrations.CreateModel(
            name='TPComment',
            fields=[
                ('basemessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Tutor.BaseMessage')),
            ],
            bases=('Tutor.basemessage',),
        ),
        migrations.CreateModel(
            name='TPMessage',
            fields=[
                ('basemessage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Tutor.BaseMessage')),
            ],
            bases=('Tutor.basemessage',),
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('baseprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='Tutor.BaseProfile')),
                ('score', models.FloatField(default=0.0, verbose_name=b'\xe8\xaf\x84\xe5\x88\x86')),
                ('state', models.CharField(default=b'F', max_length=2, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81', choices=[(b'B', b'\xe5\xbf\x99\xe7\xa2\x8c'), (b'F', b'\xe7\xa9\xba\xe9\x97\xb2')])),
                ('university', models.CharField(blank=True, max_length=30, verbose_name=b'\xe5\xa4\xa7\xe5\xad\xa6', choices=[(b'001', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe5\xb7\xa5\xe4\xb8\x9a\xe5\xa4\xa7\xe5\xad\xa6'), (b'002', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe5\xb7\xa5\xe7\xa8\x8b\xe5\xa4\xa7\xe5\xad\xa6'), (b'003', b'\xe4\xb8\x9c\xe5\x8c\x97\xe6\x9e\x97\xe4\xb8\x9a\xe5\xa4\xa7\xe5\xad\xa6'), (b'004', b'\xe9\xbb\x91\xe9\xbe\x99\xe6\xb1\x9f\xe5\xa4\xa7\xe5\xad\xa6'), (b'005', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe7\x90\x86\xe5\xb7\xa5\xe5\xa4\xa7\xe5\xad\xa6'), (b'006', b'\xe4\xb8\x9c\xe5\x8c\x97\xe5\x86\x9c\xe4\xb8\x9a\xe5\xa4\xa7\xe5\xad\xa6'), (b'007', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe5\x8c\xbb\xe7\xa7\x91\xe5\xa4\xa7\xe5\xad\xa6'), (b'008', b'\xe9\xbb\x91\xe9\xbe\x99\xe6\xb1\x9f\xe4\xb8\xad\xe5\x8c\xbb\xe8\x8d\xaf\xe5\xa4\xa7\xe5\xad\xa6'), (b'010', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe5\xb8\x88\xe8\x8c\x83\xe5\xa4\xa7\xe5\xad\xa6'), (b'011', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe5\x95\x86\xe4\xb8\x9a\xe5\xa4\xa7\xe5\xad\xa6'), (b'012', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe5\xad\xa6\xe9\x99\xa2'), (b'013', b'\xe9\xbb\x91\xe9\xbe\x99\xe6\xb1\x9f\xe5\xb7\xa5\xe7\xa8\x8b\xe5\xad\xa6\xe9\x99\xa2'), (b'014', b'\xe9\xbb\x91\xe9\xbe\x99\xe6\xb1\x9f\xe7\xa7\x91\xe6\x8a\x80\xe5\xad\xa6\xe9\x99\xa2'), (b'015', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe5\xbe\xb7\xe5\xbc\xba\xe5\x95\x86\xe5\x8a\xa1\xe5\xad\xa6\xe9\x99\xa2'), (b'016', b'\xe5\x93\x88\xe5\xb0\x94\xe6\xbb\xa8\xe4\xbd\x93\xe8\x82\xb2\xe5\xad\xa6\xe9\x99\xa2'), (b'017', b'\xe9\xbb\x91\xe9\xbe\x99\xe6\xb1\x9f\xe4\xb8\x9c\xe6\x96\xb9\xe5\xad\xa6\xe9\x99\xa2')])),
                ('major', models.CharField(max_length=40, verbose_name=b'\xe4\xb8\x93\xe4\xb8\x9a', blank=True)),
            ],
            options={
                'ordering': ['score', 'username'],
            },
            bases=('Tutor.baseprofile',),
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together=set([('subject', 'grade')]),
        ),
        migrations.AddField(
            model_name='employ',
            name='subject',
            field=models.ManyToManyField(to='Tutor.Subject', verbose_name=b'\xe7\xa7\x91\xe7\x9b\xae'),
        ),
        migrations.AddField(
            model_name='tutor',
            name='subject',
            field=models.ManyToManyField(to='Tutor.Subject', verbose_name=b'\xe7\xa7\x91\xe7\x9b\xae', blank=True),
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
            model_name='exp',
            name='tutor',
            field=models.ForeignKey(blank=True, to='Tutor.Tutor', null=True),
        ),
        migrations.AddField(
            model_name='employ',
            name='parent',
            field=models.ForeignKey(blank=True, to='Tutor.Parent', null=True),
        ),
    ]
