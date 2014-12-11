from django.conf import settings


def settings_context_processor(request):
    """
    Adds some settings' values to request context
    """

    return {
        key: getattr(settings, key) for key in ('DEBUG',)
    }
