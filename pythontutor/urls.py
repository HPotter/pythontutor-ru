from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from tutorial.views.home import home
from tutorial.views.lesson import lesson
from tutorial.views.log_events import log_user_action
from tutorial.views.problem import problem
from tutorial.views.profile import profile, register_user
from tutorial.views.statistics import statistics
from tutorial.views.tester import tester_submit
from tutorial.views.visualizer import execute, visualizer


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', home, name="home"),

    url(r'^visualizer/execute/', execute, name='visualizer_execute'),

    url(r'^visualizer/', visualizer, name='visualizer'),

    url(r'^lessons/(?P<lesson_slug>[\w\-_]+)/$', lesson, name="lesson"),

    url(r'^lessons/(?P<lesson_slug>[\w\-_]+)/problems/(?P<problem_slug>[\w\-_]+)/$', problem, name="problem"),

    url(r'^tester/submit/$', tester_submit, name='tester_submit'),

    url(r'^accounts/register/$', register_user, name='register'),

    url(r'^accounts/login/', include('social_login.urls')),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),

    url(r'^accounts/profile/$', profile, name='profile'),

    url(r'^statistics/$', statistics, name='statistics'),

    url(r'^log_user_action/$', log_user_action, name='log_user_action'),
)
