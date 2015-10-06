# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'permissions': (('view_audio', 'Can view, search, and browse audio objects'), ('download_audio', 'Download audio files (original or access copy)'), ('play_audio', 'Play audio'), ('generate_audio_access', 'Regenerate audio access copy'), ('view_researcher_audio', 'Researcher search and view'), ('download_researcher_audio', 'Researcher download'), ('play_researcher_audio', 'Researcher play audio')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedCount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'get_latest_by': 'date',
            },
            bases=(models.Model,),
        ),
    ]
