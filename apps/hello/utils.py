from .models import HttpRequest

header_filter = (
    'CONTENT_TYPE',
    'HTTP_ACCEPT',
    'HTTP_ACCEPT_CHARSET',
    'HTTP_ACCEPT_ENCODING',
    'HTTP_ACCEPT_LANGUAGE',
    'HTTP_CACHE_CONTROL',
    'HTTP_CONNECTION',
    'HTTP_HOST',
    'HTTP_KEEP_ALIVE',
    'HTTP_REFERER',
    'HTTP_USER_AGENT',
    'QUERY_STRING',
    'REMOTE_ADDR',
    'REMOTE_HOST',
    'REQUEST_METHOD',
    'SCRIPT_NAME',
    'SERVER_NAME',
    'SERVER_PORT',
    'SERVER_PROTOCOL',
    'SERVER_SOFTWARE',
)

INFO, DEBUG = range(1, 3)


def save_requests(mode=INFO, priority=False):
    """
    Default mode: INFO
    Use:
    @save_requests() (or @save_requests(mode=DEBUG))
    def main(request):
        ...
    """

    def decorator(func):
        def inner(request, *args, **kwargs):
            if not request.is_ajax():
                if mode == INFO:
                    header = {}
                    for k in header_filter:
                        if k in request.META:
                            header[k] = request.META[k]
                elif mode == DEBUG:
                    header = request.META
                else:
                    raise Exception(
                        'Use INFO or DEBUG mode in save_requests decorator'
                    )
                req = HttpRequest(ip=request.META.get('REMOTE_ADDR'),
                                  page=request.build_absolute_uri(),
                                  header=header)
                if priority:
                    req.is_priority = True
                req.save()
            return func(request, *args, **kwargs)

        return inner

    return decorator
