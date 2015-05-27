#!/bin/bash
nohup scl enable python33 -- python store_log.py  > /dev/null 2>&1 &
echo $$ > last_store_log_gpid.txt
