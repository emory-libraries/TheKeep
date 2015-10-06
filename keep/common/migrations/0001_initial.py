# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'permissions': (('arrangement_allowed', 'Access to Arrangement material is allowed.'), ('marbl_allowed', 'Access to MARBL material is allowed.')),
            },
            bases=(models.Model,),
        ),
    ]
