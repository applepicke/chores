# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Chore.user'
        db.delete_column(u'chores_chore', 'user_id')

        # Adding M2M table for field users on 'Chore'
        m2m_table_name = db.shorten_name(u'chores_chore_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('chore', models.ForeignKey(orm[u'chores.chore'], null=False)),
            ('user', models.ForeignKey(orm[u'chores.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['chore_id', 'user_id'])


    def backwards(self, orm):
        # Adding field 'Chore.user'
        db.add_column(u'chores_chore', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chores.User'], null=True),
                      keep_default=False)

        # Removing M2M table for field users on 'Chore'
        db.delete_table(db.shorten_name(u'chores_chore_users'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'chores.chore': {
            'Meta': {'object_name': 'Chore'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000', 'null': 'True'}),
            'house': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'chores'", 'to': u"orm['chores.House']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'chores'", 'null': 'True', 'to': u"orm['chores.User']"})
        },
        u'chores.house': {
            'Meta': {'object_name': 'House'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2000', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'houses'", 'symmetrical': 'False', 'to': u"orm['chores.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owned_houses'", 'null': 'True', 'to': u"orm['chores.User']"}),
            'recurs': ('django.db.models.fields.CharField', [], {'default': "'sunday'", 'max_length': '255'})
        },
        u'chores.user': {
            'Meta': {'object_name': 'User'},
            'access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'd_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'extras': ('jsonfield.fields.JSONField', [], {'default': "'{}'"}),
            'fb_user_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'sms_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sms_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['chores']