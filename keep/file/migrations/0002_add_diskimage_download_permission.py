# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disk_image',
            options={'permissions': (('view_disk_image', 'Can view, search, and browse disk images'), ('manage_disk_image_supplements', 'Can manage disk image supplemental files'), ('download_disk_image', 'Can download disk image binary content'))},
        ),
    ]
