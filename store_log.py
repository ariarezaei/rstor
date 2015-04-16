#!/usr/bin/env python
import sqlite3
import time
from subprocess import call

db = sqlite3.connect("db.sqlite3")
c = db.cursor()


def store_stat():
    context = retrieve_stats("cache1")
    read_hit_rate = str(context["read_hit_rate"]) + ","
    write_hit_rate = str(context["write_hit_rate"]) + ","
    throughput_write = str(context["throughput_write"]) + ","
    throughput_read = str(context["throughput_write"]) + ","
    mean_write_time = str(context["throughput_write"])+ ","
    mean_read_time = str(context["throughput_write"])+ ","
    read_requests = str(context["read_requests"])+ ","
    write_requests = str(context["write_requests"])
    c.execute("INSERT INTO monitor_log(time, date, read_hit_rate, write_hit_rate, throughput_write, throughput_read, mean_write_time, mean_read_time, read_requests, write_requests) VALUES (CURRENT_TIME ,CURRENT_DATE," + read_hit_rate + write_hit_rate + throughput_write + throughput_read + mean_write_time + mean_read_time + read_requests + write_requests +" )")


def retrieve_stats(cache_name):
    dic = f2d("/proc/rapidstor/"+cache_name+"/stats")
    context = {
        "reads": dic["reads"],
        "writes": dic["writes"],
        "read_hit_rate": dic["read_hit_pct"],
        "write_hit_rate": dic["write_hit_pct"],
        "read_throughput": dic["reads"]/dic["rdtime_ms"],
        "write_throughput": dic["writes"]/dic["wrtime_ms"],
        "read_mean_response": dic["rdtime_ms"]/dic["reads"],
        "read_mean_response": dic["wrtime_ms"]/dic["writes"]
    }
    return context


def f2d(file_name):
    f = open(file_name, 'r')
    d = dict()
    for line in f:
        l = line.split()
        d[l[0]] = int(l[1])
    print(d)
    return d

while True:
    store_stat()
    time.sleep(60)
db.commit()
db.close()



