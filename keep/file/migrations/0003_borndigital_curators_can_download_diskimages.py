# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


'''
Add the new download_disk_image permission to the **Born Digital Curator**
Group permissions, if the group exists.  If the group does not exist with
that name, the migration will silently proceed without error.
'''

def change_download_permission(apps, schema_editor, add=None, remove=None):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model("auth","Permission")
    try:
        bd_curator = Group.objects.get(name='Born Digital Curator')

    except Group.DoesNotExist:
        return

    # permission *should* exist since the previous migration adds it
    perm = Permission.objects.get(codename='download_disk_image',
        content_type__app_label='file')
    if add:
        bd_curator.permissions.add(perm)
    elif remove:
        bd_curator.permissions.remove(perm)
    bd_curator.save()

def add_download_permission(apps, schema_editor):
    change_download_permission(apps, schema_editor, add=True)

def remove_download_permission(apps, schema_editor):
    change_download_permission(apps, schema_editor, remove=True)


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_add_diskimage_download_permission'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_download_permission,
            reverse_code=remove_download_permission)
    ]
