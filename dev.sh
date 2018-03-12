#!/bin/bash

mate-terminal 	--tab -e "bash -c \"source ../venv/bin/activate; pip install -r requirements.txt; python manage.py migrate; python manage.py runserver 0.0.0.0:8000; /bin/bash;\""\
				--tab -e "bash -c \"sleep 4; source ../venv/bin/activate; celery worker -A chatter; /bin/bash;\""\
				--tab -e "bash -c \"sleep 6; source ../venv/bin/activate; celery -A chatter beat; /bin/bash;\""\
                --tab -e "bash -c \"sleep 8; source ../venv/bin/activate; flower -A chatter; /bin/bash;\""
