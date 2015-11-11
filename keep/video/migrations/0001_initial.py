# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VideoPerms',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'permissions': (('view_video', 'Can view, search, and browse video objects'), ('download_video', 'Download video files (original or access copy)'), ('play_video', 'Play video'), ('view_researcher_video', 'Researcher search and view'), ('download_researcher_video', 'Researcher download'), ('play_researcher_video', 'Researcher play video')),
            },
            bases=(models.Model,),
        ),
    ]
