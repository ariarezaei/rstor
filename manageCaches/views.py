from django.core.context_processors import request
from django.shortcuts import render
from subprocess import call
import json
import os.path
import os


def disks():
    call("./Disks.sh")
    lines = []
    if os.path.isfile("Disks.txt"):
        f = open("Disks.txt", 'r')
        for line in f:
            line = line.rstrip("\n")
            lines.append((line.split(" ")[0], line))
    return tuple(lines)

# Gives a list of existing caches
def cache_list():
    call("./caches.sh")
    if os.path.isfile("caches.txt"):
        f = open("caches.txt", 'r')
        c=[]
        for line in f:
            c.append(line.rstrip("\n"))
        return c
    else:
        return []

# Gives info about a specified cache
def cache_info(cache_name):
    inf = fileToDicString("/proc/rapidstor/"+cache_name+"/config");
    if inf.get("mode") == 1:
        inf["mode"] = "Write Back"
    elif inf.get("mode") == 3:
        inf["mode"] = "Write Through"
    elif inf.get("mode") == 2:
        inf["mode"] = "Read Only"
    return inf

# Changes a stat file into a dictionary of numbers
def fileToDicInt(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = int(l[1])
    return d

# Changes a stat file into a dictionary of strings
def fileToDicString(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = l[1]
    return d

# CREATE page view
from manageCaches.forms import CacheForm
def create(request):
    if request.method == u'GET':
        context={
            'form': CacheForm,
            'title' : 'RapidStor - Create a Cache',
            'caches': cache_list()
        }
        return render(request, "create.html", context)
    if request.method == u'POST':
        command = "rstor_cli create " + " -d " + request.POST.get("hdd").rstrip("\n") + " -s " + request.POST.get("ssd").rstrip("\n")
        if request.POST.get("mode", "XX") != "XX" :
            command = command + " -m " + request.POST.get("mode").rstrip("\n")
        if request.POST.get("eviction", "XX") != "XX" :
            command = command + " -p " + request.POST.get("eviction").rstrip("\n")
        if request.POST.get("block_size", "XX") != "XX" :
            command = command + " -b " + request.POST.get("block_size").rstrip("\n")
        command = command + " -c " + request.POST.get("name").rstrip("\n")
        command = command + "> status.txt"
        print(command)
        os.system(command)
        data = ""
        with open("status.txt", "r") as file:
            data = file.readlines()
        context={'status': data}
        return render(request, "status.html", context)


# EDIT page view
def edit(request, cache_name):
    if request.method == u'GET':
        inf = cache_info(cache_name)
        data={
            "name": cache_name,
            "mode": inf["mode"],
            "block_size": inf["block_size"],
            "eviction": inf["eviction"],
            "ssd": inf["ssd_name"],
            "hdd": inf["src_name"]
        }
        context={'form': CacheForm(initial=data),
                 'title': 'RapidStor - Edit a cache',
                 'cache_name':cache_name,
                 'caches': cache_list()}
        return render(request, "edit.html", context)
    if request.method == u'POST':
        command = "rstor_cli edit "
        #command = "rstor_cli edit " + " -d " + request.POST.get("hdd").rstrip("\n") + " -s " + request.POST.get("ssd").rstrip("\n")
        if request.POST.get("mode", "XX") != "XX" :
            command = command + " -m " + request.POST.get("mode").rstrip("\n")
        if request.POST.get("eviction", "XX") != "XX" :
            command = command + " -p " + request.POST.get("eviction").rstrip("\n")
        #if request.POST.get("block_size", "XX") != "XX" :
         #   command = command + " -b " + request.POST.get("block_size").rstrip("\n")
        command = command + " -c " + cache_name.rstrip("\n")
        command = command + "> status.txt"
        print(command)
        os.system(command)
        data = ""
        with open("status.txt", "r") as file:
            data = file.readlines()
        context={'status': data}
        return render(request, "status.html", context)

def remove(request, cache_name):
    if request.method == u'GET':
        command = "rstor_cli delete " + "-c " + cache_name.rstrip("\n")
        command = command + "> status.txt"
        print(command)
        os.system(command)
        data = ""
        with open("status.txt", "r") as file:
            data = file.readlines()
        context={'status': data}
        return render(request, "status.html", context)
