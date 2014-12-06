# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.functional import cached_property
import yaml


# currently totally unused model
class Language(models.Model):
    name = models.CharField('Внутреннее название языка', max_length=200, unique=True)

    def __str__(self):
        return self.name


class Problem(models.Model):
    urlname = models.SlugField('Имя для адресной строки', unique=True)
    yaml = models.TextField('YAML задачи', blank=True)
    lesson = models.ForeignKey('Lesson', verbose_name='Урок', null=True, related_name='problems')  # TODO null=False

    class Meta:
        order_with_respect_to = 'lesson'

    def __str__(self):
        return self.urlname

    @cached_property
    def yaml_data(self):
        return yaml.safe_load(self.yaml)

    @property
    def name(self):
        return self.yaml_data['name']

    @property
    def statement(self):
        return self.yaml_data['statement']

    @property
    def tests(self):
        return self.yaml_data['tests']


class Lesson(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    # Currently description is nowhere viewed
    urlname = models.SlugField('Имя для адресной строки', unique=True)
    contents = models.TextField('Текст урока', blank=True)
    problems_m2m = models.ManyToManyField(Problem, through='ProblemInLesson', blank=True, null=True, related_name='lessons_m2m')
    external_contest_link = models.URLField('Внешняя ссылка на контест', blank=True, null=True)
    course = models.ForeignKey('Course', verbose_name='Курс', null=True, related_name='lessons')  # TODO null=False

    class Meta:
        order_with_respect_to = 'course'

    def __str__(self):
        return '{self.urlname}: {self.title}'.format(self=self)

    @property
    def order_num(self):
        # TODO rename
        return self._order + 1


class ProblemInLesson(models.Model):
    problem = models.ForeignKey(Problem)
    lesson = models.ForeignKey(Lesson)
    order = models.IntegerField()


class Course(models.Model):
    OK_AC_POLICY_CHOICES = (
        (0, 'just_ok'),
        (1, 'use_accepted_instead_of_ok'),
    )

    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    urlname = models.SlugField('Имя для адресной строки', unique=True)
    lessons_m2m = models.ManyToManyField(Lesson, through='LessonInCourse', blank=True, null=True, related_name='course_m2m')
    language = models.ForeignKey(Language, blank=True, null=True)  # unused field
    ok_ac_policy = models.IntegerField(choices=OK_AC_POLICY_CHOICES)

    def __str__(self):
        return self.title


class LessonInCourse(models.Model):
    lesson = models.ForeignKey(Lesson)
    course = models.ForeignKey(Course)
    order = models.IntegerField()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # hidden = models.BooleanField(default=True)
    course = models.ForeignKey(Course, null=True, blank=True)
    # here you can add fields like 'school'

    def __str__(self):
        return '{0} {1} ({2})'.format(self.user.first_name, self.user.last_name, self.user.username)


class Submission(models.Model):
    STATUS_CHOICES = (
        (0, 'error'), # don't remove this value, or you will have a mess in your database!
        (1, 'ok'),
        (2, 'accepted'),
        (3, 'coding_style_violation'),
        (4, 'ignored'),
    )

    code = models.TextField()
    user = models.ForeignKey(User)
    problem = models.ForeignKey(Problem, db_index=True)
    status = models.IntegerField(choices=STATUS_CHOICES)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return '{self.user.first_name} {self.user.last_name} on {self.problem}: {0} ({self.time})'.format(
            self.get_status_display(), self=self)
