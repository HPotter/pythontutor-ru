from django.http.response import Http404
from annoying.decorators import render_to

from tutorial.models import Lesson, Submission


@render_to('lesson.html')
def lesson(request, lesson_slug):
    try:
        lesson = Lesson.objects.prefetch_related('course__lessons').get(urlname=lesson_slug)
    except Lesson.DoesNotExist:
        # TODO log
        # TODO (?) redirect to somewhere
        raise Http404

    if request.user.is_authenticated():
        user_solutions = {
            problem: Submission.objects.filter(user=request.user, problem=problem, status=1).order_by('time').last()
            for problem in lesson.problems.all()
        }
    else:
        user_solutions = {}

    return {
        'lesson': lesson,
        'user_solutions': {
            problem: solution for problem, solution in user_solutions.items() if solution
        }
    }
