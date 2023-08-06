import os
import redis
from mobio.libs.Singleton import Singleton
from mobio.libs.caching import LruCache
# from mobio.libs.logging import MobioLogging
import datetime
import json
import uuid
from bson import ObjectId


class StoreCacheType:
    LOCAL = 1
    REDIS = 2


class Cache:
    REDIS_URI = "{}?health_check_interval=30".format(os.environ.get("ADMIN_REDIS_URI", os.environ.get("REDIS_URI")))
    PREFIX = "m_abac"


lru_cache_redis = LruCache(
    store_type=StoreCacheType.REDIS,
    redis_uri=Cache.REDIS_URI,
    cache_prefix=Cache.PREFIX,
)


# mobio_log = MobioLogging()

class Mobio:
    ADMIN_HOST = os.environ.get("ADMIN_HOST")
    MOBIO_TOKEN = "Basic {}".format(os.environ.get('YEK_REWOP', ''))


@Singleton
class RedisClient(object):

    def __init__(self):
        self.redis_connect = redis.from_url(Cache.REDIS_URI)

    def get_connect(self):
        return self.redis_connect

    def get_value(self, key_cache):
        redis_conn = self.get_connect()
        return redis_conn.get(key_cache)

    def set_value_expire(self, key_cache, value_cache, time_seconds=3600):
        redis_conn = self.get_connect()
        redis_conn.setex(key_cache, time_seconds, value_cache)

    def delete_key(self, key_cache):
        redis_conn = self.get_connect()
        redis_conn.delete(key_cache)

    class KeyCache:
        MERCHANT_USE_ABAC = "merchant_use_abac"


class JSONEncoder(json.JSONEncoder):
    def __init__(self, format_time="%Y-%m-%dT%H:%M:%S.%fZ"):
        super().__init__()
        self.format_time = format_time

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif type(o) == datetime.date:
            a = datetime.datetime.combine(o, datetime.datetime.min.time())
            return a.strftime(self.format_time)
        elif type(o) == datetime.datetime:
            return o.strftime(self.format_time)
        elif isinstance(o, uuid.UUID):
            return str(o)
        elif isinstance(o, (bytes, bytearray)):
            return str(o, "utf-8")
        return json.JSONEncoder.default(self, o)

    def encode_data(self, o):
        if '_id' in o:
            o['_id'] = str(o['_id'])
        return json.JSONEncoder.encode(self, o)

    def json_loads(self, o):
        return json.loads(self.encode_data(o))

