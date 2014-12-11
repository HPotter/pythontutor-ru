from django.shortcuts import render

from tutorial.models import Course, Lesson, Problem, Submission
from tutorial.views import need_login


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

    saved_code = get_best_saved_code(request.user, problem_slug)

    return render(request, 'problem.html', locals())
