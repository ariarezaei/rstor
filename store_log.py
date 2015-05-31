#!/usr/bin/env python
import sqlite3
import time
from subprocess import call
import threading

db = sqlite3.connect("db.sqlite3")
c = db.cursor()

last_reads = dict()
last_writes = dict()
last_read_time = dict()
last_write_time = dict()
last_ssd_reads = dict()
lsdt_ssd_writes = dict()


def store_stat(cache):
    context = retrieve_stats(cache)
    read_hit_rate = str(context["read_hit_rate"]) + ","
    write_hit_rate = str(context["write_hit_rate"]) + ","
    throughput_write = str(context["write_throughput"]) + ","
    throughput_read = str(context["read_throughput"]) + ","
    mean_write_time = str(context["write_mean_response"])+ ","
    mean_read_time = str(context["read_mean_response"])+ ","
    read_requests = str(context["reads"]) + ","
    write_requests = str(context["writes"]) + ","
    cur_read_time = str(context["cur_read_time"]) + ","
    cur_write_time =  str(context["cur_write_time"]) + ","
    cur_reads = str(context["cur_reads"]) + ","
    cur_writes = str(context["cur_writes"])
    cache = "'" + cache + "',"
    command= "INSERT INTO monitor_log(datetime, cache, read_hit_rate, write_hit_rate, throughput_write, throughput_read, mean_write_time, mean_read_time, read_requests, write_requests, cur_write_time, cur_read_time, cur_reads, cur_writes) VALUES (datetime('now', 'localtime') ," + cache  + read_hit_rate + write_hit_rate + throughput_write + throughput_read + mean_write_time + mean_read_time + read_requests + write_requests + cur_write_time + cur_read_time + cur_reads + cur_writes + " )"
    return command


def retrieve_stats(cache_name):
    dic = f2d("/proc/rapidstor/"+cache_name+"/stats")
    if cache_name not in last_reads:
        last_reads[cache_name] = dic["reads"]
        last_writes[cache_name] = dic["writes"]
        last_read_time[cache_name] = dic["rdtime_ms"]
        last_write_time[cache_name] = dic["wrtime_ms"]
	last_ssd_reads[cache_name] = dic["ssd_reads"]
	last_ssd_writes[cache_name] = dic["ssd_writes"]
    context = {
        "reads": dic["ssd_reads"] - last_ssd_reads[cache_name],
        "writes": dic["ssd_writes"] - last_ssd_writes[cache_name],
        "read_hit_rate": dic["read_hit_pct"],
        "write_hit_rate": dic["write_hit_pct"],
        "read_throughput": 0 if dic["rdtime_ms"] == last_read_time[cache_name] else 1000*(dic["reads"] - last_reads[cache_name])/(dic["rdtime_ms"] - last_read_time[cache_name]),
        "write_throughput": 0 if dic["wrtime_ms"] == last_write_time[cache_name] else 1000*(dic["writes"] - last_writes[cache_name])/(dic["wrtime_ms"] - last_write_time[cache_name]),
        "read_mean_response": 0 if dic["reads"] == last_reads[cache_name] else (dic["rdtime_ms"] - last_read_time[cache_name])/(dic["reads"] - last_reads[cache_name]),
        "write_mean_response": 0 if dic["writes"] == last_writes[cache_name] else (dic["wrtime_ms"] - last_write_time[cache_name])/(dic["writes"] - last_writes[cache_name]),
        "cur_reads": dic["reads"] - last_reads[cache_name],
        "cur_writes": dic["writes"] - last_writes[cache_name],
        "cur_read_time": dic["rdtime_ms"] - last_read_time[cache_name],
        "cur_write_time": dic["wrtime_ms"] - last_write_time[cache_name]
    }
    last_reads[cache_name] = dic["reads"]
    last_writes[cache_name] = dic["writes"]
    last_read_time[cache_name] = dic["rdtime_ms"]
    last_write_time[cache_name] = dic["wrtime_ms"]
    last_ssd_reads[cache_name] = dic["ssd_reads"]
    last_ssd_writes[cache_name] = dic["ssd_writes"]

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
        c.execute(command)
        db.commit()
    time.sleep(5)
db.close()

def store():
  threading.Timer(5, store).start()
   call('./caches.sh')
   f = open('caches.txt', 'r')

   for line in f:
       cache = line.rstrip("\n")
       print(cache)
       command = store_stat(cache)
       c.execute(command)
       db.commit()


store()



