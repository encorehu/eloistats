#!/usr/bin/env python
import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options
from tornado import gen

import momoko

db_database = os.environ.get('MOMOKO_TEST_DB', 'pooldb')
db_user = os.environ.get('MOMOKO_TEST_USER', 'eloipool')
db_password = os.environ.get('MOMOKO_TEST_PASSWORD', '')
db_host = os.environ.get('MOMOKO_TEST_HOST', 'localhost')
db_port = os.environ.get('MOMOKO_TEST_PORT', 5432)
enable_hstore = True if os.environ.get('MOMOKO_TEST_HSTORE', False) == '1' else False
dsn = 'dbname=%s user=%s password=%s host=%s port=%s' % (
    db_database, db_user, db_password, db_host, db_port)

from settings import settings
from urls import url_patterns

class TornadoBoilerplate(tornado.web.Application):
    def __init__(self):
        tornado.web.Application.__init__(self, url_patterns, **settings)


def main():
    app = TornadoBoilerplate()

    app.db = momoko.Pool(
        dsn=dsn,
        size=1,
        max_size=3,
        setsession=("SET TIME ZONE UTC",),
        raise_connect_errors=False,
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
