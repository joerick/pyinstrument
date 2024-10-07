import time

from django.http import HttpResponse


def hello_world(request):
    # do some useless work to delay this call a bit
    y = 1
    for x in range(1, 10000):
        y *= x
    time.sleep(0.1)

    return HttpResponse("Hello, world!")  # type: ignore
