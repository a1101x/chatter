import json

from django.contrib.auth import get_user_model
from elasticsearch.helpers import bulk
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import Q

from apps.chat.message import Message
from apps.repositories.search import MessageIndex
from chatter.celery import app as celery_app


class MessageSaver(object):
    """
    Class for working with messages in elasticsearch.
    """

    @staticmethod
    @celery_app.task(name='apps.chat.save_message')
    def save_message(rows):
        """
        Save message to the elasticsearch.
        """
        MessageIndex.init()
        msg = [MessageIndex(**row).to_dict(include_meta=True) for row in rows]
        es = connections.get_connection()
        bulk(es, msg)
