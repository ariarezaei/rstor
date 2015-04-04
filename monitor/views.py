from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render

def index(request):

    if request.method == u'POST':
        return HttpResponseNotFound("Sorry. We could not find the page you requested. Please check the address and try again.")

    context = {
        'title': "Rapid Storage Monitoring Portal"
    }

    return render(request, 'index.html', context)
