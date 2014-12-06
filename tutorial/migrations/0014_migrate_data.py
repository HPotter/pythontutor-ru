# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings

from ..yaml_extended import dump, quoted, folded


ABSOLUTE_PATH_TO_PROBLEMS = settings.ABSOLUTE_PREFIX + 'problems/'
ABSOLUTE_PATH_TO_LESSONS = settings.ABSOLUTE_PREFIX + 'lessons/'


def parse_problem(filename):
    ret = {}
    ret['tests'] = []
    ret['answers'] = []

    curParts = []
    curDelimiter = None

    def processRecord():
        if curDelimiter == 'Name:':
            ret['name'] = '\n'.join(curParts).strip()
        elif curDelimiter == 'Statement:':
            ret['statement'] = ' '.join(curParts).strip()
        elif curDelimiter == 'Test:':
            ret['tests'].append('\n'.join(curParts).strip())
        elif curDelimiter == 'Answer:':
            ret['answers'].append('\n'.join(curParts).strip())


    with open(filename, 'r', encoding='utf-8') as problem_file:
        for line in problem_file.readlines():
            # only strip TRAILING spaces and not leading spaces
            line = line.rstrip()

            # comments are denoted by a leading '//', so ignore those lines.
            # Note that I don't use '#' as the comment token since sometimes I
            # want to include Python comments in the skeleton code.
            if line.startswith('//'):
                continue

            # special-case one-liners:
            if line.startswith('MaxInstructions:'):
                ret['max_instructions'] = int(line.split(':')[1])
                continue # move to next line


            if line in ('Name:', 'Statement:', 'Test:', 'Answer:'):
                processRecord()
                curDelimiter = line
                curParts = []
            else:
                curParts.append(line)

    # don't forget to process the FINAL record
    processRecord()

    assert len(ret['tests']) == len(ret['answers'])

    return ret


def load_problem(problem):
    return parse_problem(ABSOLUTE_PATH_TO_PROBLEMS + problem.filename)


def load_lesson(lesson):
    filename = ABSOLUTE_PATH_TO_LESSONS + lesson.filename

    with open(filename, 'r', encoding='utf-8') as lesson_file:
        return lesson_file.read()


class Migration(DataMigration):

    def forwards(self, orm):
        # migrate Problem
        for problem in orm.Problem.objects.all():
            # migrate contents
            problem_data = load_problem(problem)
            problem_yaml_data = {
                'name': quoted(problem_data['name']),
                'statement': folded(problem_data['statement']),
                'tests': [
                    {
                        'input': folded(test_input.strip()),
                        'answer': folded(test_answer.strip()),
                    } for test_input, test_answer
                    in zip(problem_data['tests'], problem_data['answers'])
                ],
            }

            if 'max_instructions' in problem_data:
                problem_yaml_data['max_instructions'] = int(problem_data['max_instructions'])

            problem.yaml = dump(problem_yaml_data)

            problem.save()

        # migrate Lesson
        for lesson in orm.Lesson.objects.all():
            # migrate contents
            lesson.contents = load_lesson(lesson)

            lesson.save()

        # TODO remove files from system or/and replace them with fixture
        # not sure if migration is good place for it

    def backwards(self, orm):
        # it's real, but hard
        # raise RuntimeError("Cannot reverse this migration.")
        pass

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'object_name': 'Permission', 'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_set'", 'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'db_table': "'django_content_type'", 'object_name': 'ContentType', 'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)"},
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
            'lessons': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'through': "orm['tutorial.LessonInCourse']", 'symmetrical': 'False', 'to': "orm['tutorial.Lesson']"}),
            'ok_ac_policy': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'urlname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'tutorial.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'tutorial.lesson': {
            'Meta': {'object_name': 'Lesson'},
            'contents': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'external_contest_link': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'filename': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problems': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'null': 'True', 'through': "orm['tutorial.ProblemInLesson']", 'symmetrical': 'False', 'to': "orm['tutorial.Problem']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'urlname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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
            'filename': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'urlname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
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
            'user': ('django.db.models.fields.related.OneToOneField', [], {'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['tutorial']
    symmetrical = True
