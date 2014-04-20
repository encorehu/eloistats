import json
import tornado.web

from tornado import gen
import momoko

import logging
logger = logging.getLogger('boilerplate.' + __name__)


class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    @property
    def db(self):
        return self.application.db

    @property
    def schema(self):
        return self.application.schema

    @property
    def server_id(self):
        return self.application.server_id

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg

    @gen.coroutine
    def get_stats_cache(self, type_id, query_hash):
        sql = 'select * from %s.stats_cache ' % self.schema
        sql = sql + ' where type_id=%s and query_hash=%s and expire_time > NOW() '

        cursor = yield momoko.Op(self.db.execute, sql, (type_id, query_hash))
        result = cursor.fetchone()
        logger.debug(cursor.query)
        logger.debug(result)
        if result:
            raise gen.Return(result.data.decode('base64'))
        raise gen.Return('')

    @gen.coroutine
    def set_stats_cache(self, type_id, query_hash, data, expireseconds):

        #apc_store("wizstats_cache_".$type."_".$hash,$data, $expireseconds);

        # clean cache
        sql = 'delete from %s.stats_cache where expire_time < NOW()' % self.schema
        cursor = yield momoko.Op(self.db.execute, sql)

        b64data = data.encode('utf-8').encode('base64')
        sql = 'insert into %s.stats_cache (query_hash, type_id, create_time, expire_time, data) ' % self.schema
        sql = sql + " VALUES (%s, %s, NOW(), NOW()+'%s seconds', %s)"
        cursor = yield momoko.Op(self.db.execute, sql, (query_hash, type_id, expireseconds, data))

    @gen.coroutine
    def update_stats_cache(self, type_id, query_hash, data, expireseconds):
        b64data = data.encode('utf-8').encode('base64')
        sql = "update %s.stats_cache " % self.schema
        sql = sql + " set create_time=NOW(), expire_time=NOW()+'%s seconds', data=%s where type_id=%s and query_hash=%s"
        cursor = yield momoko.Op(self.db.execute, sql, (expireseconds, data, type_id, query_hash))

    @gen.coroutine
    def get_context_data(self, *args, **kwargs):

        # if nodata in database, set default values, to fix many Notice: Undefined variable...
        # the risk is may cause something wrong, may the calculate is not right
        roundshares = 0
        sharesperunit = 1
        blockheight = 1
        latestconfirms = 0
        latestconfirms = 0
        roundduration = 1
        netdiff = 1

        datanew = 0
        phash = ""

        livedata = yield self.get_stats_cache(5, 'livedata.json')
        logger.debug(livedata)

        if livedata != '':
            instantjsondec = json.loads(livedata)
            phash = instantjsondec.get('hashratepretty','')
            roundduration = instantjsondec.get('roundduration','')
            sharesperunit = instantjsondec.get('sharesperunit','')
            netdiff = instantjsondec.get('network_difficulty','')
            roundshares = instantjsondec.get('roundsharecount','')
            blockheight = instantjsondec.get('lastblockheight','')
            latestconfirms = instantjsondec.get('lastconfirms','')
            datanew = 0
        else:
            pass

        tline = '{"sharesperunit":%(sharesperunit),"roundsharecount":%(roundshares)s,"lastblockheight":%(blockheight)s,"lastconfirms":%(latestconfirms)s,"roundduration":%(roundduration)s,"hashratepretty":"%(phash)s","network_difficulty":%(netdiff)s}' % kwargs

        if datanew:
            # cache this for 30 seconds, should be good enough
            result = yield self.set_stats_cache(5, "livedata.json", tline, 30)

        raise gen.Return(**kwargs)
