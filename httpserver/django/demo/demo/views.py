import time
from django.http import HttpResponse


def index(request):
    time.sleep(0.1)
    return HttpResponse('<p>Hello World</p>')
