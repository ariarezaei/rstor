#!/bin/bash

gpid=$(cat last_server_gpid.txt)
echo $gpid
kill -TERM -$gpid
