# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'permissions': (('view_collection', 'Can view, search, and browse collection objects'), ('view_researcher_collection', 'Search, view collections with researcher content')),
            },
            bases=(models.Model,),
        ),
    ]
