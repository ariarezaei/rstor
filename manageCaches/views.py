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
        form = CacheForm(request.POST)

        if form.is_valid():
            command = "rstor_cli create " + " -d " + request.POST.get("hdd").rstrip("\n") + " -s " + request.POST.get("ssd").rstrip("\n")
            if request.POST.get("mode", "XX") != "XX" :
                command = command + " -m " + request.POST.get("mode").rstrip("\n")
            if request.POST.get("eviction", "XX") != "XX" :
                command = command + " -p " + request.POST.get("eviction").rstrip("\n")
            if request.POST.get("block_size", "XX") != "XX" :
                command = command + " -b " + request.POST.get("block_size").rstrip("\n")
            command = command + " -c " + request.POST.get("name").rstrip("\n")
            command = command + "> status.txt"
            os.system(command)
            (status, message) = parse_status_message('status.txt')
            if status == 'success':
                context={
                    'form': CacheForm,
                    'title': 'RapidStor - Create a Cache',
                    'caches': cache_list(),
                    'success_message': message
                    }
                return render(request, "create.html", context)
            else:
                context={
                    'form': form,
                    'title': 'RapidStor - Create a Cache',
                    'caches': cache_list(),
                    'error_message': message
                }
                return render(request, 'create.html', context)
        else:
            error_message = parse_status_message('status.txt')
            print(error_message)
            context = {
                'form': form,
                'title': 'RapidStor - Create a Cache',
                'caches': cache_list(),
                'error_message': 'The form was invalid.'
            }
            return render(request, "create.html", context)


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
        form = CacheForm(request.POST)
        if form.is_valid():
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
            os.system(command)
            (status, message) = parse_status_message('status.txt')
            if status == 'success':
                context={
                    'cache_name': cache_name,
                    'form': form,
                    'title': 'RapidStor - Edit a cache',
                    'caches': cache_list(),
                    'success_message': message
                }
                return render(request, "edit.html", context)
            else:
                context = {
                    'cache_name': cache_name,
                    'form': form,
                    'title': 'RapidStor - Edit a cache',
                    'caches': cache_list(),
                    'error_message': message
                }
                return render(request, "edit.html", context)
        else:
            context = {
                'cache_name': cache_name,
                'form': form,
                'title': 'RapidStor - Edit a cache',
                'caches': cache_list(),
                'error_message': 'Form is invalid'
            }
            return render(request, 'edit.html', context)

def remove(request, cache_name):
    if request.method == u'GET':
        command = "rstor_cli delete " + "-c " + cache_name.rstrip("\n")
        command = command + "> status.txt"
        print(command)
        os.system(command)
        context={
            'title': 'RapidStor - Status Page',
            'caches': cache_list(),
            'success_message': message
        }
        Log.objects.filter(cache=cache_name).delete()
        return render(request, "status.html", context)


def parse_status_message(file):
    res = ""
    with open(file, 'r') as status_file:
        for line in status_file:
            if ':' in line or '=' in line or 'None' in line:
                continue
            elif line == "":
                continue
            else:
                res += line.replace('\n', '<br>')
    print(res)
    if 'Success' in res or 'success' in res:
        return ('success', res)
    else:
        return ('fail', res)
