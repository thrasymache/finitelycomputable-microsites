from django.http import HttpResponse

def hello_world(request):
    return HttpResponse('Django says "hello, world"\n')
