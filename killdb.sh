#!/bin/bash

gpid=$(cat last_store_log_gpid.txt)
echo $gpid
kill -TERM -$gpid
