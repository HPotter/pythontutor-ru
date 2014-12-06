from collections import OrderedDict

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from tutorial.models import Course, Lesson, Problem, Submission
from tutorial.lessons import get_sorted_lessons, load_lesson
from tutorial.problems import get_sorted_problems, load_problem
from tutorial.views import DEFAULT_COURSE, need_login


def get_best_saved_code(user, problem_urlname):
    problem = Problem.objects.get(urlname=problem_urlname)

    submissions = Submission.objects.filter(user=user, problem=problem).order_by('-time')
    submission = None
    for s in submissions:
        if s.get_status_display() == 'ok':
            submission = s
            break

    if not submission and len(submissions) > 0:
        submission = submissions[0]

    return submission.code if submission else ''


def problem_status(submission_statuses):
    if 1 in submission_statuses:
        return 'solved'
    elif 2 in submission_statuses:
        return 'accepted'
    elif 0 in submission_statuses:
        return 'unsolved'
    else:
        return ''


@need_login
def problem(request, lesson_slug, problem_slug):
    lesson = Lesson.objects.get(urlname=lesson_slug)
    problem = Problem.objects.get(urlname=problem_slug)

    lesson_problems = [
        (
            problem,
            problem_status(problem.submissions.values_list('status', flat=True))
        ) for problem in lesson.problems.all()
    ]

    # for problem in lesson.problems:
    #     if request.user.is_authenticated():
    #         statuses = [submission.get_status_display() for submission
    #                 in Submission.objects.filter(user=request.user, problem=problem['db_object'])]
    #     else:
    #         statuses = []
    #
    #     if 'ok' in statuses:
    #         problem['status'] = 'solved'
    #     elif 'accepted' in statuses:
    #         problem['status'] = 'accepted'
    #     elif 'error' in statuses:
    #         problem['status'] = 'unsolved'
    #     else:
    #         problem['status'] = ''

    saved_code = get_best_saved_code(request.user, problem_slug)

    # tests_examples = []
    # for test_input, test_output in zip(problem['tests'], problem['answers']):
    #     tests_examples.append({'input': test_input, 'output': test_output})

    return render(request, 'problem.html', locals())
