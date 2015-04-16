from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import json
from django.shortcuts import HttpResponse
from subprocess import call

def index(request):

    if request.method == u'POST':
        return HttpResponseNotFound("Sorry. We could not find the page you requested. Please check the address and try again.")

    context = {
        'title': "Rapid Storage Monitoring Portal"
    }

    return render(request, 'index.html', context)

def instant_stat(request):

    if request.method == u'GET':
        context = retrieve_stats("cache1")
        return HttpResponse(json.dump(context), content_type="application/json")




def retrieve_stats(cache_name):
    call("cat /proc/rapidstor/"+cache_name+"/stats > tmp_stat.txt")
    dic = f2d("tmp_stat.txt")
    context = {
        "reads": dic["reads"],
        "writes": dic["writes"],
        "read_hit_rate": dic["read_hit_rate"],
        "write_hit_rate": dic["write_hit_rate"],
        "read_throughput": dic["reads"]/dic["rdtime_ms"],
        "write_throughput": dic["writes"]/dic["wrtime_ms"],
        "read_mean_response": dic["rdtieme"]/dic["reads"],
        "read_mean_response": dic["wrtieme"]/dic["writes"]
    }
    return context

def f2d(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = int(l[1])
    return d





