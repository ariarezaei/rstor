from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import json
from django.shortcuts import HttpResponse
from monitor.models import Log
from subprocess import *
import math
import random

# Main view for index page
def index(request):

    if request.method == u'POST':
        return HttpResponseNotFound("Sorry. We could not find the page you requested. Please check the address and try again.")

    #TODO: find all caches and put it in the array below
    caches = [
        'cache1',
        'cache2',
        'cache3',
        'cache_imba',
        'cache_nakazaki'
    ]

    context = {
        'title': "Rapid Storage Monitoring Portal",
        'caches': caches
    }

    return render(request, 'index.html', context)

# Create some dummy cache configurations for testing purposes
def dummy_cache_config(request, cache_name):
    if request.method == u'GET':
        context = {
            'main_disk_name': 'Disk1',
            'main_disk_size': '1024 MB',
            'cache_disk_name': 'Disk3',
            'cache_type': 'LRU',
            'cache_size': '128 MB',
            'block_size': '4096 KB',
            'cache_state': '<span class="text-success">NORMAL</span>'
        }

        return HttpResponse(json.dumps(context), content_type="application/json")

# Retrieves cache mode (Write back, ...) from a command line
def cache_mode(mode):

    if mode == '1':
        return "Write Back"
    if mode == '3':
        return "Write Through"
    if mode == '2':
        return "Read Only"
    return "Unknown"

# Stylize the state and gives it color based on NORMAL/DEGRADED/FAILED
def styled_state(state):

    if state == "normal":
        return '<span class="text-success">NORMAL</span>'
    elif state == "degraded":
        return '<span class="text-warning">DEGRADED</span>'
    elif state == "failed":
        return '<span class="text-danger">FAILED</span>'
    else:
        return '<span class"text-danger">UNKNOWN (' + state + ')</span>'

def caches():
    call("./caches.sh")
    f = open(caches.txt, 'r')
    c=[]
    for line in f:
        c.append(line.rstrip("\n"))
    return c

# Retrieves cache stat from CMD
def cache_config(request, cache_name):
    config = fileToDicString("/proc/rapidstor/" + cache_name + "/config")
    return HttpResponse(json.dumps({
        'main_disk_name': config['src_name'],
        'main_disk_size': config['src_size'],
        'cache_disk_name': config['ssd_name'],
        'cache_size': config['ssd_size'],
        'cache_type': cache_mode(config['mode']),
        'cache_state': styled_state(config['state']),
        'block_size': config['block_size']
    }), content_type="application/json")

# Main function for retrieving, chooses from three functions below
def instant_stat(request, cache_name):

    if request.method == u'GET':
        context = retrieve_db(cache_name, cache_name)
        return HttpResponse(json.dumps(context), content_type="application/json")

# Creates dummy cache stats for testing purposes
def dummy_retrieve_stats(cache_name):
    context = {
        "reads": round(random.random()*100),
        "writes": round(random.random()*100),
        "read_hit_rate": round(random.random()*100),
        "write_hit_rate": round(random.random()*100),
        "throughput_read": round(random.random()*100),
        "throughput_write": round(random.random()*100),
        "read_mean_response": round(random.random()*100),
        "write_mean_response": round(random.random()*100)
    }
    return context

# Retrieves cache stats from CMD
def retrieve_stats(cache_name):
    dic = fileToDicInt("/proc/rapidstor/"+cache_name+"/stats")
    context = {
        "reads": dic["reads"],
        "writes": dic["writes"],
        "read_hit_rate": dic["read_hit_pct"],
        "write_hit_rate": dic["write_hit_pct"],
        "throughput_read": dic["reads"]/dic["rdtime_ms"],
        "throughput_write": dic["writes"]/dic["wrtime_ms"],
        "read_mean_response": dic["rdtime_ms"]/dic["reads"],
        "write_mean_response": dic["wrtime_ms"]/dic["writes"]
    }
    return context

# Retrieves cache stats from DB
def retrieve_db(request, cache_name):
    l = Log.objects.latest('id')
    context = l.__dict__
    print(context)
    return context

# Changes a stat file into a dictionary
def fileToDicInt(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = int(l[1])
    return d

def fileToDicString(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = l[1]
    return d
