#!/usr/bin/env python
import sqlite3
import time
from subprocess import call

db = sqlite3.connect("db.sqlite3")
c = db.cursor()


def store_stat(cache):
    context = retrieve_stats(cache)
    read_hit_rate = str(context["read_hit_rate"]) + ","
    write_hit_rate = str(context["write_hit_rate"]) + ","
    throughput_write = str(context["write_throughput"]) + ","
    throughput_read = str(context["read_throughput"]) + ","
    mean_write_time = str(context["write_mean_response"])+ ","
    mean_read_time = str(context["read_mean_response"])+ ","
    read_requests = str(context["reads"])+ ","
    write_requests = str(context["writes"])
    command= "INSERT INTO monitor_log(time, date, cache, read_hit_rate, write_hit_rate, throughput_write, throughput_read, tot_write_time, tot_read_time, read_requests, write_requests) VALUES (CURRENT_TIME ,CURRENT_DATE," + "'" + cache + "'," + read_hit_rate + write_hit_rate + throughput_write + throughput_read + mean_write_time + mean_read_time + read_requests + write_requests +" )"
    return command


def retrieve_stats(cache_name):
    dic = f2d("/proc/rapidstor/"+cache_name+"/stats")
    context = {
        "reads": dic["ssd_reads"],
        "writes": dic["ssd_writes"],
        "read_hit_rate": dic["read_hit_pct"],
        "write_hit_rate": dic["write_hit_pct"],
        "read_throughput": dic["reads"]/dic["rdtime_ms"]*1000,
        "write_throughput": dic["writes"]/dic["wrtime_ms"]*1000,
        "read_mean_response": dic["rdtime_ms"]/dic["reads"],
        "write_mean_response": dic["wrtime_ms"]/dic["writes"]
    }
    return context


def f2d(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = int(l[1])
    return d

while True:
    call('./caches.sh')
    f = open('caches.txt', 'r')

    for line in f:
        cache = line.rstrip("\n")
        print(cache)
        command = store_stat(cache)
        print(command)
        c.execute(command)
        db.commit()

    time.sleep(5)
db.close()



