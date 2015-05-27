#!/bin/bash
nohup scl enable python33 -- python manage.py runserver 0.0.0.0:80  > /dev/null 2>&1 &
echo $$ > last_server_gpid.txt
