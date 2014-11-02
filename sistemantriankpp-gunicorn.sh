#!/bin/bash
NAME="sistemantriankpp"
DJANGODIR=/media/MyDATA/Arsip/Programming/Webapps/DjangoProjects/sistemantriankpp
SOCKFILE=/media/MyDATA/Arsip/Programming/Webapps/run/sistemantriankpp-gunicorn.sock
USER=webapps
GROUP=webapps
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=sistemantriankpp.settings
DJANGO_WSGI_MODULE=sistemantriankpp.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source ../../bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec ../../bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=unix:$SOCKFILE \
  --log-level=debug --max-requests 1 \
  --log-file=/media/MyDATA/Arsip/Programming/Webapps/DjangoProjects/logs/sistemantrian-gunicorn.log
