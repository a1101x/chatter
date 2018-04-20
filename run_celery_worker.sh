#!/bin/sh

-c "celery worker -A chatter"
-c "celery -A chatter beat"
