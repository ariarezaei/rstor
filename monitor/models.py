
# Create your models here.
from django.db import models

# Create your models here.


class Log(models.Model):
    cache = models.StringField(default="")
    time = models.TimeField()
    date = models.DateField()
    read_hit_rate = models.FloatField(default=0)
    write_hit_rate = models.FloatField(default=0)
    throughput_write = models.FloatField(default=0)
    throughput_read = models.FloatField(default=0)
    tot_write_time = models.FloatField(default=0)
    tot_read_time = models.FloatField(default=0)
    read_requests = models.IntegerField(default=0)
    write_requests = models.IntegerField(default=0)