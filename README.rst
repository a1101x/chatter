==================
Running backend
==================

System packages
---------------
First, you need to install postgresql server, redis, elasticsearch, and rabbitmq.


Database
--------
You need to create a postgresql user chatter with password chatter, and a database chatter.

.. code:: sh

  sudo su - postgres -c psql

.. code:: postgres

  CREATE USER chatter WITH CREATEDB PASSWORD 'chatter';
  CREATE DATABASE chatter ENCODING 'UTF8';
  GRANT ALL ON DATABASE chatter TO chatter;


PostGis
--------
.. code:: sh

  sudo -u <user_name> psql chatter

.. code:: postgres

  ALTER ROLE <user_name> SUPERUSER;
  CREATE EXTENSION postgis;


Server
--------
Run migrations:

.. code:: sh

  ./manage.py migrate

Creating a superuser: You can add a user with

.. code:: sh

  ./manage.py createsuperuser

Django shell (for experimenting/debugging):

.. code:: sh

  ./manage.py shell

Run server

.. code:: sh

  ./manage.py runserver

| A list of api methods at http://localhost:8000/swagger/
| Django admin is at http://localhost:8000/admin/


Celery:
--------
.. code:: sh

  celery worker -A chatter --without-gossip --without-mingle --without-heartbeat
  celery -A chatter beat


Content
-------
The content api requires an elasticsearch server running on localhost.