# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Lesson.contents'
        db.add_column('tutorial_lesson', 'contents',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'Lesson.urlname'
        db.alter_column('tutorial_lesson', 'urlname', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True))

        # Changing field 'Lesson.external_contest_link'
        db.alter_column('tutorial_lesson', 'external_contest_link', self.gf('django.db.models.fields.URLField')(null=True, max_length=200))
        # Adding field 'Problem.yaml'
        db.add_column('tutorial_problem', 'yaml',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'Problem.urlname'
        db.alter_column('tutorial_problem', 'urlname', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True))

        # Changing field 'Course.urlname'
        db.alter_column('tutorial_course', 'urlname', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True))

    def backwards(self, orm):
        # Deleting field 'Lesson.contents'
        db.delete_column('tutorial_lesson', 'contents')


        # Changing field 'Lesson.urlname'
        db.alter_column('tutorial_lesson', 'urlname', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True))

        # Changing field 'Lesson.external_contest_link'
        db.alter_column('tutorial_lesson', 'external_contest_link', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))
        # Deleting field 'Problem.yaml'
        db.delete_column('tutorial_problem', 'yaml')


        # Changing field 'Problem.urlname'
        db.alter_column('tutorial_problem', 'urlname', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True))

        # Changing field 'Course.urlname'
        db.alter_column('tutorial_course', 'urlname', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'related_name': "'user_set'", 'to': "orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tutorial.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['tutorial.Language']", 'blank': 'True'}),
            'lessons': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tutorial.Lesson']", 'null': 'True', 'blank': 'True', 'through': "orm['tutorial.LessonInCourse']"}),
            'ok_ac_policy': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'urlname': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'})
        },
        'tutorial.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'unique': 'True'})
        },
        'tutorial.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'contents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external_contest_link': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problems': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['tutorial.Problem']", 'null': 'True', 'blank': 'True', 'through': "orm['tutorial.ProblemInLesson']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'urlname': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'})
        },
        'tutorial.lessonincourse': {
            'Meta': {'object_name': 'LessonInCourse'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Lesson']"}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        'tutorial.problem': {
            'Meta': {'object_name': 'Problem'},
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'urlname': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'yaml': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'tutorial.probleminlesson': {
            'Meta': {'object_name': 'ProblemInLesson'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Lesson']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Problem']"})
        },
        'tutorial.submission': {
            'Meta': {'object_name': 'Submission'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Problem']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tutorial.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['tutorial.Course']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['tutorial']