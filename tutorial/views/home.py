from annoying.decorators import render_to

from tutorial.models import Course


@render_to('index.html')
def home(request):
    return {
        'courses': Course.objects.prefetch_related('lessons').all()
    }
