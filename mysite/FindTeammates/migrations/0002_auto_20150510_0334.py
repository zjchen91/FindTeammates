# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FindTeammates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('University', models.CharField(max_length=200)),
                ('Professor', models.CharField(max_length=100)),
                ('courseName', models.CharField(max_length=200)),
                ('Capacity', models.IntegerField(default=0)),
                ('groupSize', models.IntegerField(default=0)),
                ('courseDescription', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('messageType', models.IntegerField(default=0)),
                ('content', models.CharField(max_length=200)),
                ('messageStatus', models.IntegerField(default=0)),
                ('date', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='skillOverlap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numOfOverlap', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='student_course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('courseID', models.ForeignKey(to='FindTeammates.Course')),
                ('studentID', models.ForeignKey(to='FindTeammates.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='student_team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentID', models.ForeignKey(to='FindTeammates.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='stuJoinTeamHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('teamName', models.CharField(max_length=100)),
                ('teamDescription', models.CharField(max_length=500)),
                ('Status', models.IntegerField(default=0)),
                ('Size', models.IntegerField(default=0)),
                ('courseID', models.ForeignKey(to='FindTeammates.Course')),
                ('ownerID', models.ForeignKey(to='FindTeammates.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='teamInviteStuHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inviteeID', models.ForeignKey(related_name='invitee', to='FindTeammates.Student')),
                ('inviterID', models.ForeignKey(related_name='inviter', to='FindTeammates.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.AddField(
            model_name='stujointeamhistory',
            name='joineeTeamID',
            field=models.ForeignKey(to='FindTeammates.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='stujointeamhistory',
            name='joinerID',
            field=models.ForeignKey(to='FindTeammates.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='student_team',
            name='teamID',
            field=models.ForeignKey(to='FindTeammates.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='skilloverlap',
            name='studentID',
            field=models.ForeignKey(to='FindTeammates.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='skilloverlap',
            name='teamID',
            field=models.ForeignKey(to='FindTeammates.Team'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='receiverID',
            field=models.ForeignKey(related_name='receiver', to='FindTeammates.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='senderID',
            field=models.ForeignKey(related_name='sender', to='FindTeammates.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='teamID',
            field=models.ForeignKey(to='FindTeammates.Team'),
            preserve_default=True,
        ),
    ]
