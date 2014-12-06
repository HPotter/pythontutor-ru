# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Problem.lesson'
        db.add_column('tutorial_problem', 'lesson',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutorial.Lesson'], null=True),
                      keep_default=False)

        # Adding field 'Problem._order'
        db.add_column('tutorial_problem', '_order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Lesson.course'
        db.add_column('tutorial_lesson', 'course',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutorial.Course'], null=True),
                      keep_default=False)

        # Adding field 'Lesson._order'
        db.add_column('tutorial_lesson', '_order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Problem.lesson'
        db.delete_column('tutorial_problem', 'lesson_id')

        # Deleting field 'Problem._order'
        db.delete_column('tutorial_problem', '_order')

        # Deleting field 'Lesson.course'
        db.delete_column('tutorial_lesson', 'course_id')

        # Deleting field 'Lesson._order'
        db.delete_column('tutorial_lesson', '_order')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')"},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Group']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'related_name': "'user_set'"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'tutorial.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['tutorial.Language']", 'null': 'True'}),
            'lessons_m2m': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tutorial.Lesson']", 'through': "orm['tutorial.LessonInCourse']", 'blank': 'True', 'related_name': "'course_m2m'", 'null': 'True', 'symmetrical': 'False'}),
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
            'Meta': {'ordering': "('_order',)", 'object_name': 'Lesson'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'contents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Course']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external_contest_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problems_m2m': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tutorial.Problem']", 'through': "orm['tutorial.ProblemInLesson']", 'blank': 'True', 'related_name': "'lessons_m2m'", 'null': 'True', 'symmetrical': 'False'}),
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
            'Meta': {'ordering': "('_order',)", 'object_name': 'Problem'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lesson': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Lesson']", 'null': 'True'}),
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
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tutorial.Problem']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tutorial.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'to': "orm['tutorial.Course']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['tutorial']