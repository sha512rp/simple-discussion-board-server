from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from board.models import Thread
from board.serializers import ThreadSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def thread_list(request):
    """List all threads, or create a new thread."""
    if request.method == 'GET':
        threads = Thread.objects.all()
        serializer = ThreadSerializer(threads, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ThreadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """Retrieve, update or delete a thread."""
    try:
        thread = Thread.objects.get(pk=pk)
    except Thread.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ThreadSerializer(thread)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ThreadSerializer(thread, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        thread.delete()
        return HttpResponse(status=204)
