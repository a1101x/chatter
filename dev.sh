#!/bin/bash

mate-terminal 	--tab -e "bash -c \"source ../venv/bin/activate; python manage.py runserver 0.0.0.0:8000;\""\
				--tab -e "bash -c \"source ../venv/bin/activate; daphne -p 8001 chatter.asgi:application;\""\
				--tab -e "bash -c \"source ../venv/bin/activate; celery worker -A chatter;\""\
				--tab -e "bash -c \"source ../venv/bin/activate; celery -A chatter beat;\""\
                --tab -e "bash -c \"sleep 2; source ../venv/bin/activate; flower -A chatter;\""
