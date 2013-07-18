import redis
import cPickle
import datetime
import time


class RedisEveAPICacheHandler(object):

    def __init__(self, debug=False):
        self.debug = debug
        self.r = redis.StrictRedis()

    def log(self, what):
        if self.debug:
            print "[%s] %s" % (datetime.datetime.now().isoformat(), what)

    def retrieve(self, host, path, params):
        key = hash((host, path, frozenset(params.items())))

        cached = self.r.get(key)
        if cached is None:
            self.log("%s: not cached, fetching from server..." % path)
            return None
        else:
            cached = cPickle.loads(cached)
            if time.time() < cached[0]:
                self.log("%s: returning cached document" % path)
                return cached[1]
            self.log("%s: cache expired, purging !" % path)
            self.r.delete(key)

    def store(self, host, path, params, doc, obj):
        key = hash((host, path, frozenset(params.items())))

        cachedFor = obj.cachedUntil - obj.currentTime
        if cachedFor:
            self.log("%s: cached (%d seconds)" % (path, cachedFor))

            cachedUntil = time.time() + cachedFor
            cached = self.r.set(key, cPickle.dumps((cachedUntil, doc), -1))
