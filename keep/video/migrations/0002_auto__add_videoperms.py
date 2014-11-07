# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VideoPerms'
        db.create_table(u'video_videoperms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'video', ['VideoPerms'])


    def backwards(self, orm):
        # Deleting model 'VideoPerms'
        db.delete_table(u'video_videoperms')


    models = {
        u'video.videoperms': {
            'Meta': {'object_name': 'VideoPerms'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['video']