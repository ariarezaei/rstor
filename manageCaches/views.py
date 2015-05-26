from django.core.context_processors import request
from django.shortcuts import render
from django import forms
from subprocess import call
import json
import os.path
import os
# Create your views here.

MODE_CHOICES = (
        ("wb", "wb"),
        ("wt", "wt"),
        ("ro", "ro")
    )

PODE_CHOICES = (
        ("smart", "smart"),
        ("rand", "rand"),
        ("fifo", "fifo"),
        ("lru", "lru")
    )
BODE_CHOICES= (
        ("2048", "2048"),
        ("4096", "4096"),
        ("8192", "8192")
)

def disks():
    call("./Disks.sh")
    lines = []
    if os.path.isfile("Disks.txt"):
        f = open("Disks.txt", 'r')
        for line in f:
            line = line.rstrip("\n")
            lines.append((line.split(" ")[0], line))
    return tuple(lines)


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


def cache_info(cache_name):
    inf = fileToDicString("/proc/rapidstor/"+cache_name+"/config");
    if inf.get("mode") == 1:
        inf["mode"] = "Write Back"
    elif inf.get("mode") == 3:
        inf["mode"] = "Write Through"
    elif inf.get("mode") == 2:
        inf["mode"] = "Read Only"
    return inf



def fileToDicInt(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = int(l[1])
    return d

# Changes a stat file into a String Dictionary
def fileToDicString(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = l[1]
    return d



class CacheForm(forms.Form):
    name = forms.CharField(label='Cache Name', max_length=30, required=True)
    mode = forms.ChoiceField(label="mode",
        choices=MODE_CHOICES,
        initial='',
        widget=forms.Select(),
        required=False)
    block_size = forms.ChoiceField(label="block size",
        choices=BODE_CHOICES,
        initial='',
        widget=forms.Select(),
        required=False)
    eviction = forms.ChoiceField(label="eviction",
        choices=PODE_CHOICES,
        initial='',
        widget=forms.Select(),
        required=False)
    ssd = forms.ChoiceField(label="ssd",
        choices=disks(),
        initial='',
        widget=forms.Select(),
        required=True)
    hdd = forms.ChoiceField(label="src",
        choices=disks(),
        initial='',
        widget=forms.Select(),
        required=True)


def create(request):
    if request.method == u'GET':
        context={'form': CacheForm}
        return render(request, "create.html", context)
    if request.method == u'POST':
        command = "rstor_cli create " + " -d " + request.POST.get("hdd") + " -s " + request.POST.get("ssd")
        if request.POST.get("mode", "XX") != "XX" :
            command = command + " -m " + request.POST.get("mode")
        if request.POST.get("eviction", "XX") != "XX" :
            command = command + " -p " + request.POST.get("eviction")
        if request.POST.get("block_size", "XX") != "XX" :
            command = command + " -b " + request.POST.get("block_size")
        command = command + " -c " + request.POST.get("name")
        command = command + "> status.txt"
        print(command)
        os.system(command)
        data = ""
        with open("status.txt", "r") as file:
            data = file.readlines()
        context={'status': data}
        return render(request, "status.html", context)



def edit(request, cache_name):
    if request.method == u'GET':
        inf = cache_info(cache_name)
        data={
            "name": cache_name,
            "mode": inf["mode"],
            "block_size": inf["block_size"],
            "eviction": inf["eviction"],
            "ssd": inf["ssd_name"],
            "src": inf["src_name"]
        }
        context={'form': CacheForm(initial=data)}
        return render(request, "create.html", context)
    if request.method == u'POST':
        command = "rstor_cli edit " + " -d " + request.POST.get("hdd") + " -s " + request.POST.get("ssd")
        if request.POST.get("mode", "XX") != "XX" :
            command = command + " -m " + request.POST.get("mode")
        if request.POST.get("eviction", "XX") != "XX" :
            command = command + " -p " + request.POST.get("eviction")
        if request.POST.get("block_size", "XX") != "XX" :
            command = command + " -b " + request.POST.get("block_size")
        command = command + " -c " + request.POST.get("name")
        print(command)
        os.system(command)
        data = ""
        with open("status.txt", "r") as file:
            data = file.readlines()
        context={'status': data}
        return render(request, "status.html", context)

def remove(request, cache_name):
    if request.method == u'GET':
        command = "rstor_cli delete " \
                  "-c " + cache_name
        print(command)
        os.system(command)
        data = ""
        with open("status.txt", "r") as file:
        data = file.readlines()
        context={'status': data}
        return render(request, "status.html", context)
