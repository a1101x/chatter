import abc

from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from redis import StrictRedis

REDIS_API_SETTINGS = {
    'host': settings.REDIS_CHAT_URL_HOST,
    'port': settings.REDIS_CHAT_URL_PORT,
    'db': settings.REDIS_CHAT_URL_DB,
    'charset': settings.REDIS_CHAT_CHARSET,
    'decode_responses': settings.REDIS_CHAT_DECODE_RESPONSES
}

ELASTICSEARCH_API_SETTINGS = {
    'hosts': settings.ELASTICSEARCH_CHAT_HOST
}


class RedisInterfaceBase(abc.ABC):
    """
    Base interface for redis.
    """
    def __init__(self, *args, **kwargs):
        self.redis = StrictRedis(**REDIS_API_SETTINGS)

    def append_message(self, room, user, created, message, status, tags):
        raise NotImplementedError

    def get_messages(self, room, limit):
        raise NotImplementedError


class ElasticInterfaceBase(abc.ABC):
    """
    Base interface for elasticsearch.
    """
    def __init__(self, *args, **kwargs):
        self.es = Elasticsearch(**ELASTICSEARCH_API_SETTINGS)
        self.search = Search(using=self.es, index='Messages')

    def append_message(self, room, user, created, message, status, tags):
        """
        Save message to the elasticsearch index.
        """
        raise NotImplementedError

    def get_messages(self, room, limit):
        """
        Get messages from elastic for selected room.
        """
        raise NotImplementedError
