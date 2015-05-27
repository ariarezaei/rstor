#!/bin/bash
scl enable python33 -- python manage.py makemigrations
scl enable python33 -- python manage.py migrate
scl enable python33 -- python manage.py syncdb
