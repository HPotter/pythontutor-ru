from django.http.response import Http404
from annoying.decorators import render_to

from tutorial.models import Lesson


@render_to('lesson.html')
def lesson(request, lesson_slug):
    try:
        lesson = Lesson.objects.prefetch_related('course__lessons').get(urlname=lesson_slug)
    except Lesson.DoesNotExist:
        # TODO log
        # TODO (?) redirect to somewhere
        raise Http404

    return {
        'lesson': lesson,
    }
